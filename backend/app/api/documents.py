"""Documentation ingestion API routes."""

from typing import Any, List, Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_session
from app.models import Project, Specification, SpecificationKind

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload")
async def upload_document(
    project_id: int,
    file: UploadFile = File(...),
    kind: str = Query("API", pattern="^(API|UI|DATA|SECURITY)$"),
    version: str = Query("1.0.0"),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Upload and ingest a documentation file."""
    # Verify project exists
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Read file content
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Failed to read file: {str(e)}"
        )

    # Create specification from document
    spec = Specification(
        project_id=project_id,
        kind=SpecificationKind(kind),
        version=version,
        doc_md=content_str,
        links=[],
    )

    session.add(spec)
    await session.commit()
    await session.refresh(spec)

    return {
        "status": "success",
        "message": f"Document '{file.filename}' ingested successfully",
        "spec_id": spec.id,
        "project_id": project_id,
        "kind": kind,
        "size_bytes": len(content),
    }


@router.post("/ingest/markdown")
async def ingest_markdown(
    project_id: int,
    title: str,
    content: str,
    kind: str = Query("API", pattern="^(API|UI|DATA|SECURITY)$"),
    version: str = Query("1.0.0"),
    links: List[str] = Query([]),
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Ingest markdown documentation directly via API."""
    # Verify project exists
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Create specification
    spec = Specification(
        project_id=project_id,
        kind=SpecificationKind(kind),
        version=version,
        doc_md=content,
        links=links,
    )

    session.add(spec)
    await session.commit()
    await session.refresh(spec)

    return {
        "status": "success",
        "message": f"Documentation '{title}' ingested successfully",
        "spec_id": spec.id,
        "project_id": project_id,
        "kind": kind,
        "version": version,
    }


@router.post("/bulk-ingest")
async def bulk_ingest_documents(
    documents: List[dict],
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    """Bulk ingest multiple documentation items."""
    results = []
    errors = []

    for doc in documents:
        try:
            project_id = doc.get("project_id")
            if not project_id:
                errors.append({"doc": doc, "error": "Missing project_id"})
                continue

            # Verify project exists
            project = await session.get(Project, project_id)
            if not project:
                errors.append(
                    {"doc": doc, "error": f"Project {project_id} not found"}
                )
                continue

            # Create specification
            spec = Specification(
                project_id=project_id,
                kind=SpecificationKind(doc.get("kind", "API")),
                version=doc.get("version", "1.0.0"),
                doc_md=doc.get("content", ""),
                links=doc.get("links", []),
            )

            session.add(spec)
            await session.flush()
            await session.refresh(spec)

            results.append(
                {
                    "spec_id": spec.id,
                    "project_id": project_id,
                    "kind": spec.kind,
                }
            )

        except Exception as e:
            errors.append({"doc": doc, "error": str(e)})

    await session.commit()

    return {
        "status": "success" if not errors else "partial",
        "ingested": len(results),
        "results": results,
        "errors": errors,
        "total_attempted": len(documents),
    }


@router.get("/list")
async def list_documents(
    project_id: Optional[int] = Query(None),
    kind: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session),
) -> List[dict[str, Any]]:
    """List ingested documentation."""
    query = select(Specification)

    if project_id:
        query = query.where(Specification.project_id == project_id)
    if kind:
        query = query.where(Specification.kind == kind)

    result = await session.execute(query)
    specs = result.scalars().all()

    return [
        {
            "id": spec.id,
            "project_id": spec.project_id,
            "kind": spec.kind,
            "version": spec.version,
            "content_length": len(spec.doc_md) if spec.doc_md else 0,
            "links_count": len(spec.links) if spec.links else 0,
        }
        for spec in specs
    ]


@router.get("/{doc_id}")
async def get_document(
    doc_id: int, session: AsyncSession = Depends(get_session)
) -> dict[str, Any]:
    """Get a specific document's content."""
    spec = await session.get(Specification, doc_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": spec.id,
        "project_id": spec.project_id,
        "kind": spec.kind,
        "version": spec.version,
        "content": spec.doc_md,
        "links": spec.links,
    }


@router.delete("/{doc_id}")
async def delete_document(
    doc_id: int, session: AsyncSession = Depends(get_session)
) -> dict[str, str]:
    """Delete an ingested document."""
    spec = await session.get(Specification, doc_id)
    if not spec:
        raise HTTPException(status_code=404, detail="Document not found")

    await session.delete(spec)
    await session.commit()

    return {"status": "success", "message": f"Document {doc_id} deleted"}
