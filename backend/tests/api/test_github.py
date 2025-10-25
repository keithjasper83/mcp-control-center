"""Tests for GitHub API endpoints."""

import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_get_github_config_no_token(client: AsyncClient):
    """Test getting GitHub config when no token is configured."""
    response = await client.get("/api/github/config")
    assert response.status_code == 200
    data = response.json()
    assert "enabled" in data
    assert "has_token" in data


@pytest.mark.asyncio
async def test_list_repositories_no_token(client: AsyncClient):
    """Test listing repositories without GitHub token."""
    response = await client.get("/api/github/repositories")
    assert response.status_code == 401
    assert "GitHub token not configured" in response.json()["detail"]


@pytest.mark.asyncio
async def test_sync_from_github_no_token(client: AsyncClient):
    """Test syncing from GitHub without token."""
    response = await client.post("/api/github/sync")
    assert response.status_code == 401
    assert "GitHub token not configured" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_repository_no_token(client: AsyncClient):
    """Test creating a repository without GitHub token."""
    response = await client.post(
        "/api/github/repositories?name=test-repo&description=Test"
    )
    assert response.status_code == 401
    assert "GitHub token not configured" in response.json()["detail"]
