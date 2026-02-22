import httpx
import logging
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

class JulesClient:
    def __init__(self, api_key: str, base_url: str = "https://jules.googleapis.com/v1alpha"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    async def _request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            url = f"{self.base_url}/{path.lstrip('/')}"
            logger.debug(f"Making {method} request to {url}")
            try:
                response = await client.request(method, url, headers=self.headers, json=json, timeout=30.0)
                response.raise_for_status()
                if response.status_code == 204 or not response.text:
                    return {}
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                raise

    async def list_sources(self) -> Dict[str, Any]:
        return await self._request("GET", "sources")

    async def get_source(self, source_name: str) -> Dict[str, Any]:
        """source_name should be like 'sources/github/owner/repo'"""
        return await self._request("GET", source_name)

    async def list_sessions(self, page_size: Optional[int] = None, page_token: Optional[str] = None) -> Dict[str, Any]:
        params = []
        if page_size:
            params.append(f"pageSize={page_size}")
        if page_token:
            params.append(f"pageToken={page_token}")

        path = "sessions"
        if params:
            path += "?" + "&".join(params)

        return await self._request("GET", path)

    async def create_session(
        self,
        source: str,
        instruction: str,
        branch: Optional[str] = None,
        require_plan_approval: bool = False,
        auto_pr: bool = False
    ) -> Dict[str, Any]:
        data = {
            "source": source,
            "instruction": instruction,
        }
        if branch:
            data["branch"] = branch
        if require_plan_approval:
            data["requirePlanApproval"] = require_plan_approval
        if auto_pr:
            data["autoPr"] = auto_pr
        return await self._request("POST", "sessions", json=data)

    async def get_session(self, session_name: str) -> Dict[str, Any]:
        """session_name should be like 'sessions/12345'"""
        return await self._request("GET", session_name)

    async def delete_session(self, session_name: str) -> Dict[str, Any]:
        """session_name should be like 'sessions/12345'"""
        return await self._request("DELETE", session_name)

    async def approve_plan(self, session_name: str) -> Dict[str, Any]:
        """session_name should be like 'sessions/12345'"""
        return await self._request("POST", f"{session_name}:approvePlan", json={})

    async def send_message(self, session_name: str, prompt: str) -> Dict[str, Any]:
        """session_name should be like 'sessions/12345'"""
        return await self._request("POST", f"{session_name}:sendMessage", json={"prompt": prompt})

    async def list_activities(
        self,
        session_name: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """session_name should be like 'sessions/12345'"""
        params = []
        if page_size:
            params.append(f"pageSize={page_size}")
        if page_token:
            params.append(f"pageToken={page_token}")

        path = f"{session_name}/activities"
        if params:
            path += "?" + "&".join(params)

        return await self._request("GET", path)

    async def get_activity(self, activity_name: str) -> Dict[str, Any]:
        """activity_name should be like 'sessions/12345/activities/67890'"""
        return await self._request("GET", activity_name)
