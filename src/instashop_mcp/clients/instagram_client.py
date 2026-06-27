# src/instashop_mcp/clients/instagram_client.py
import httpx
from ..config import Config


class InstagramClient:

    GRAPH_INSTAGRAM_BASE = "https://graph.instagram.com"
    GRAPH_FACEBOOK_BASE = "https://graph.facebook.com"

    def __init__(self, config: Config):
        self.config = config
        # Single shared async client — reuse connections for performance
        self._client = httpx.AsyncClient(timeout=30.0)

    def _build_url(self, path: str, use_fb: bool) -> str:
        base = self.GRAPH_FACEBOOK_BASE if use_fb else self.GRAPH_INSTAGRAM_BASE
        return f"{base}/{self.config.ig_api_version}{path}"

    async def get(
        self,
        path: str,
        params: dict | None = None,
        use_fb: bool = True
    ) -> dict:

        url = self._build_url(path, use_fb)
        params = params or {}
        params["access_token"] = self.config.ig_access_token

        response = await self._client.get(url, params=params)

        # raise_for_status() converts 4xx/5xx HTTP codes to exceptions
        # The server's call_tool() handler catches these and returns error text
        response.raise_for_status()
        return response.json()

    async def post(
        self,
        path: str,
        params: dict | None = None,
        json_body: dict | None = None,
        use_fb: bool = False
    ) -> dict:

        url = self._build_url(path, use_fb)
        params = params or {}
        params["access_token"] = self.config.ig_access_token

        response = await self._client.post(url, params=params, json=json_body)
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the underlying HTTP connection pool. Call during server shutdown."""
        await self._client.aclose()