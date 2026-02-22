import pytest
import respx
import httpx
from src.jules_client import JulesClient

@pytest.mark.asyncio
async def test_list_sources():
    client = JulesClient(api_key="test-key")

    with respx.mock:
        respx.get("https://jules.googleapis.com/v1alpha/sources").mock(
            return_value=httpx.Response(200, json={"sources": [{"name": "sources/github/owner/repo"}]})
        )

        response = await client.list_sources()
        assert response == {"sources": [{"name": "sources/github/owner/repo"}]}

@pytest.mark.asyncio
async def test_create_session():
    client = JulesClient(api_key="test-key")

    with respx.mock:
        respx.post("https://jules.googleapis.com/v1alpha/sessions").mock(
            return_value=httpx.Response(201, json={"name": "sessions/123"})
        )

        response = await client.create_session(source="sources/github/owner/repo", instruction="test")
        assert response == {"name": "sessions/123"}
