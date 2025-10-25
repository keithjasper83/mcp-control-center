"""Tests for project API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_projects_empty(client: AsyncClient):
    """Test listing projects when database is empty."""
    response = await client.get("/api/projects")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    """Test creating a new project."""
    project_data = {
        "name": "Test Project",
        "repo_url": "https://github.com/test/project",
        "language_matrix": {"python": "3.12"},
        "tags": ["test"],
    }
    response = await client.post("/api/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["repo_url"] == "https://github.com/test/project"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    """Test getting a specific project."""
    # Create a project first
    project_data = {"name": "Test Project", "tags": []}
    create_response = await client.post("/api/projects", json=project_data)
    project_id = create_response.json()["id"]

    # Get the project
    response = await client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id
    assert data["name"] == "Test Project"


@pytest.mark.asyncio
async def test_get_nonexistent_project(client: AsyncClient):
    """Test getting a project that doesn't exist."""
    response = await client.get("/api/projects/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    """Test updating a project."""
    # Create a project first
    project_data = {"name": "Original Name", "tags": []}
    create_response = await client.post("/api/projects", json=project_data)
    project_id = create_response.json()["id"]

    # Update the project
    update_data = {"name": "Updated Name"}
    response = await client.patch(f"/api/projects/{project_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
