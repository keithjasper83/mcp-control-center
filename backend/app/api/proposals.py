"""Proposals API routes."""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Proposal, Rule, RuleGate
from app.services.mcp_client import get_mcp_client, MCPClient

router = APIRouter(prefix="/api/proposals", tags=["proposals"])


@router.get("", response_model=List[Proposal])
async def list_proposals(
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[Proposal]:
    """List proposals with optional filters."""
    query = select(Proposal)

    if project_id:
        query = query.where(Proposal.project_id == project_id)
    if status:
        query = query.where(Proposal.status == status)

    result = await session.execute(query)
    return result.scalars().all()


@router.post("", response_model=Proposal)
async def create_proposal(
    proposal: Proposal, session: AsyncSession = Depends(get_session)
) -> Proposal:
    """Create a new proposal."""
    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)
    return proposal


@router.get("/{proposal_id}", response_model=Proposal)
async def get_proposal(
    proposal_id: int, session: AsyncSession = Depends(get_session)
) -> Proposal:
    """Get a specific proposal."""
    proposal = await session.get(Proposal, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found")
    return proposal


@router.post("/preview")
async def preview_proposal(
    proposal_data: dict, session: AsyncSession = Depends(get_session)
) -> dict[str, Any]:
    """Preview and validate a proposal."""
    project_id = proposal_data.get("project_id")
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    # Get all FAIL rules for the project
    result = await session.execute(
        select(Rule).where(
            Rule.project_id == project_id, Rule.enabled == True, Rule.gate == RuleGate.FAIL
        )
    )
    fail_rules = result.scalars().all()

    # Simple validation - check if any FAIL rules exist
    violations = []
    for rule in fail_rules:
        # In a real implementation, you would run actual checks here
        # For now, we just note which rules would be checked
        violations.append(
            {
                "rule": rule.name,
                "category": rule.category,
                "message": f"Would check: {rule.policy_md[:100]}...",
            }
        )

    return {
        "valid": len(violations) == 0,
        "violations": violations,
        "summary": proposal_data.get("summary_md", ""),
        "project_id": project_id,
    }


@router.post("/submit")
async def submit_proposal(
    proposal_data: dict,
    session: AsyncSession = Depends(get_session),
    mcp_client: MCPClient = Depends(get_mcp_client),
) -> dict[str, Any]:
    """Submit a proposal after validating against rules."""
    project_id = proposal_data.get("project_id")
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    # Get all FAIL rules for the project
    result = await session.execute(
        select(Rule).where(
            Rule.project_id == project_id, Rule.enabled == True, Rule.gate == RuleGate.FAIL
        )
    )
    fail_rules = result.scalars().all()

    # Check for violations
    violations = []
    for rule in fail_rules:
        # In a real implementation, run actual validation
        pass

    if violations:
        raise HTTPException(
            status_code=400,
            detail={"message": "Proposal violates quality gates", "violations": violations},
        )

    # Create proposal in database
    proposal = Proposal(
        project_id=project_id,
        summary_md=proposal_data.get("summary_md", ""),
        patch_manifest_json=proposal_data.get("patch_manifest_json", {}),
        linked_features=proposal_data.get("linked_features", []),
        status="Submitted",
    )
    session.add(proposal)
    await session.commit()
    await session.refresh(proposal)

    # Submit to MCP if available
    try:
        mcp_response = await mcp_client.post_proposal(str(project_id), proposal_data)
        return {
            "status": "submitted",
            "proposal_id": proposal.id,
            "mcp_response": mcp_response,
        }
    except Exception as e:
        # Proposal saved locally even if MCP submission fails
        return {
            "status": "submitted_locally",
            "proposal_id": proposal.id,
            "mcp_error": str(e),
        }
