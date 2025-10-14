"""MCP client service for integration with MCP servers."""

from typing import Any

import httpx

from app.config import get_settings


class MCPClient:
    """Client for interacting with MCP servers."""

    def __init__(self) -> None:
        """Initialize MCP client."""
        self.settings = get_settings()
        self.base_url = self.settings.MCP_BASE_URL
        self.token = self.settings.MCP_TOKEN

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def list_projects(self) -> list[dict[str, Any]]:
        """List all projects from MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/projects",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def list_features(self, project: str) -> list[dict[str, Any]]:
        """List features for a project from MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/projects/{project}/features",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def get_feature(self, feature_id: str) -> dict[str, Any]:
        """Get a specific feature from MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/features/{feature_id}",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def post_proposal(self, project: str, payload: dict[str, Any]) -> dict[str, Any]:
        """Post a proposal to MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/projects/{project}/proposals",
                json=payload,
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def list_tools(self) -> list[dict[str, Any]]:
        """List available tools from MCP server."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tools",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()


def get_mcp_client() -> MCPClient:
    """Get MCP client instance."""
    return MCPClient()
