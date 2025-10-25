"""Reports API routes."""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Project, Rule, RuleCategory
from app.services.soc_checks import analyze_project_soc

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/soc")
async def get_soc_report(
    project_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Get Separation of Concerns report for a project."""
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get SoC rules for this project
    result = await session.execute(
        select(Rule).where(
            Rule.project_id == project_id,
            Rule.category == RuleCategory.SOC,
            Rule.enabled.is_(True),
        )
    )
    soc_rules = result.scalars().all()

    # Perform SoC analysis if we have a project path
    soc_analysis = {}
    if project.repo_url:
        # In a real implementation, you would clone/access the repo
        # For now, return structure showing what would be analyzed
        soc_analysis = {
            "analysis_available": False,
            "message": "Project analysis requires local repository access",
            "repo_url": project.repo_url,
        }

    return {
        "project_id": project_id,
        "project_name": project.name,
        "soc_rules_count": len(soc_rules),
        "soc_rules": [
            {
                "name": rule.name,
                "policy": rule.policy_md,
                "gate": rule.gate,
            }
            for rule in soc_rules
        ],
        "analysis": soc_analysis,
        "recommendations": [
            "Enable grimp analysis for Python projects",
            "Define layer architecture (UI -> Service -> Domain -> Infrastructure)",
            "Check for circular dependencies regularly",
        ],
    }


@router.get("/quality")
async def get_quality_report(
    project_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Get quality gate report for a project."""
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get all rules for this project
    result = await session.execute(
        select(Rule).where(Rule.project_id == project_id, Rule.enabled == True)
    )
    rules = result.scalars().all()

    # Group rules by category
    rules_by_category = {}
    for rule in rules:
        category = rule.category
        if category not in rules_by_category:
            rules_by_category[category] = []
        rules_by_category[category].append(
            {
                "name": rule.name,
                "gate": rule.gate,
                "policy": rule.policy_md[:100] + "..." if len(rule.policy_md) > 100 else rule.policy_md,
            }
        )

    # Quality gate summary (placeholder - would run actual checks)
    quality_gates = {
        "ruff": {
            "status": "not_run",
            "message": "Run 'ruff check .' to analyze code style",
        },
        "mypy": {
            "status": "not_run",
            "message": "Run 'mypy .' to check type annotations",
        },
        "pytest": {
            "status": "not_run",
            "message": "Run 'pytest' to execute tests",
        },
        "bandit": {
            "status": "not_run",
            "message": "Run 'bandit -r .' to check for security issues",
        },
    }

    return {
        "project_id": project_id,
        "project_name": project.name,
        "total_rules": len(rules),
        "rules_by_category": rules_by_category,
        "quality_gates": quality_gates,
        "recommendations": [
            "Set up CI/CD to run quality checks automatically",
            "Increase test coverage to ≥85%",
            "Fix all FAIL gate violations before merging",
        ],
    }


@router.get("/violations")
async def get_violations(
    project_id: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Get current rule violations for a project."""
    if not project_id:
        raise HTTPException(status_code=400, detail="project_id is required")

    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # In a real implementation, this would run actual checks
    # For now, return structure
    violations = []

    return {
        "project_id": project_id,
        "project_name": project.name,
        "violations": violations,
        "total_violations": len(violations),
        "status": "passed" if not violations else "failed",
    }
