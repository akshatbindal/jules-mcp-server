import logging
from typing import Optional
from mcp.server.fastmcp import FastMCP
from .jules_client import JulesClient
from .secrets import get_jules_api_key

logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP("Jules")

def get_client() -> JulesClient:
    api_key = get_jules_api_key()
    if not api_key:
        logger.error("JULES_API_KEY not found.")
        raise ValueError("Jules API key not found. Please ensure Secret Manager is configured or JULES_API_KEY is set.")
    return JulesClient(api_key)

@mcp.tool()
async def list_sources():
    """Lists all available sources (repositories) connected to Jules."""
    client = get_client()
    return await client.list_sources()

@mcp.tool()
async def get_source(source_name: str):
    """Gets details of a single source.
    source_name should be the full resource name, e.g., 'sources/github/owner/repo'
    """
    client = get_client()
    return await client.get_source(source_name)

@mcp.tool()
async def list_sessions(page_size: Optional[int] = None, page_token: Optional[str] = None):
    """Lists all coding sessions."""
    client = get_client()
    return await client.list_sessions(page_size, page_token)

@mcp.tool()
async def create_session(
    source: str,
    instruction: str,
    branch: Optional[str] = None,
    require_plan_approval: bool = False,
    auto_pr: bool = False
):
    """Creates a new coding session.

    Args:
        source: Full resource name of the source (e.g., 'sources/github/owner/repo')
        instruction: The task for Jules to perform
        branch: The branch to work on (defaults to main)
        require_plan_approval: If true, Jules will wait for plan approval before proceeding
        auto_pr: If true, Jules will automatically create a Pull Request upon completion
    """
    client = get_client()
    return await client.create_session(source, instruction, branch, require_plan_approval, auto_pr)

@mcp.tool()
async def get_session(session_name: str):
    """Gets a single session's details and status.
    session_name should be the full resource name, e.g., 'sessions/12345'
    """
    client = get_client()
    return await client.get_session(session_name)

@mcp.tool()
async def delete_session(session_name: str):
    """Deletes a session.
    session_name should be the full resource name, e.g., 'sessions/12345'
    """
    client = get_client()
    return await client.delete_session(session_name)

@mcp.tool()
async def approve_plan(session_name: str):
    """Approves a pending plan in a session.
    session_name should be the full resource name, e.g., 'sessions/12345'
    """
    client = get_client()
    return await client.approve_plan(session_name)

@mcp.tool()
async def send_message(session_name: str, prompt: str):
    """Sends a message/feedback to an active session.
    session_name should be the full resource name, e.g., 'sessions/12345'
    prompt: The message content
    """
    client = get_client()
    return await client.send_message(session_name, prompt)

@mcp.tool()
async def list_activities(session_name: str, page_size: Optional[int] = None, page_token: Optional[str] = None):
    """Lists activities for a session to monitor progress.
    session_name should be the full resource name, e.g., 'sessions/12345'
    """
    client = get_client()
    return await client.list_activities(session_name, page_size, page_token)

@mcp.tool()
async def get_activity(activity_name: str):
    """Gets a single activity's details.
    activity_name should be the full resource name, e.g., 'sessions/12345/activities/67890'
    """
    client = get_client()
    return await client.get_activity(activity_name)
