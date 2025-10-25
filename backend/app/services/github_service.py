"""GitHub integration service for syncing projects."""

from typing import Any, Optional

import httpx

from app.config import get_settings


class GitHubService:
    """Service for interacting with GitHub API."""

    def __init__(self, token: Optional[str] = None) -> None:
        """Initialize GitHub service."""
        self.settings = get_settings()
        self.token = token or self.settings.GITHUB_TOKEN
        self.base_url = "https://api.github.com"

    def _get_headers(self) -> dict[str, str]:
        """Get request headers with authentication."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    async def list_repositories(self, user: Optional[str] = None) -> list[dict[str, Any]]:
        """List repositories for authenticated user or specified user."""
        async with httpx.AsyncClient() as client:
            if user:
                url = f"{self.base_url}/users/{user}/repos"
            else:
                url = f"{self.base_url}/user/repos"

            response = await client.get(
                url, headers=self._get_headers(), params={"per_page": 100}, timeout=30.0
            )
            response.raise_for_status()
            return response.json()

    async def get_repository(self, owner: str, repo: str) -> dict[str, Any]:
        """Get details of a specific repository."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def create_repository(
        self, name: str, description: str = "", private: bool = False
    ) -> dict[str, Any]:
        """Create a new GitHub repository."""
        async with httpx.AsyncClient() as client:
            data = {
                "name": name,
                "description": description,
                "private": private,
                "auto_init": True,
            }
            response = await client.post(
                f"{self.base_url}/user/repos",
                headers=self._get_headers(),
                json=data,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def list_repository_languages(self, owner: str, repo: str) -> dict[str, int]:
        """Get programming languages used in a repository."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/languages",
                headers=self._get_headers(),
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()


def get_github_service(token: Optional[str] = None) -> GitHubService:
    """Get GitHub service instance."""
    return GitHubService(token)
