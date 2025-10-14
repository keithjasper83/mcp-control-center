"""Tests for feature API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_features_empty(client: AsyncClient):
    """Test listing features when database is empty."""
    response = await client.get("/api/features")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_feature(client: AsyncClient):
    """Test creating a new feature."""
    # Create a project first
    project_data = {"name": "Test Project", "tags": []}
    project_response = await client.post("/api/projects", json=project_data)
    project_id = project_response.json()["id"]

    # Create a feature
    feature_data = {
        "project_id": project_id,
        "title": "Test Feature",
        "description_md": "Test description",
        "status": "DRAFT",
        "priority": 1,
        "labels": ["test"],
    }
    response = await client.post("/api/features", json=feature_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Feature"
    assert data["project_id"] == project_id
    assert "id" in data


@pytest.mark.asyncio
async def test_filter_features_by_project(client: AsyncClient):
    """Test filtering features by project."""
    # Create two projects
    project1 = await client.post("/api/projects", json={"name": "Project 1", "tags": []})
    project2 = await client.post("/api/projects", json={"name": "Project 2", "tags": []})
    project1_id = project1.json()["id"]
    project2_id = project2.json()["id"]

    # Create features for each project
    await client.post(
        "/api/features",
        json={"project_id": project1_id, "title": "Feature 1", "labels": []},
    )
    await client.post(
        "/api/features",
        json={"project_id": project2_id, "title": "Feature 2", "labels": []},
    )

    # Filter by project1
    response = await client.get(f"/api/features?project_id={project1_id}")
    assert response.status_code == 200
    features = response.json()
    assert len(features) == 1
    assert features[0]["project_id"] == project1_id
