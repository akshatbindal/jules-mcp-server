import logging
import os
from fastapi import FastAPI
from dotenv import load_dotenv
from .server import mcp

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jules MCP Server")

# Mount the MCP SSE app
# This will expose /sse and /messages endpoints
app.mount("/mcp", mcp.sse_app())

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": "Jules MCP Server is running",
        "mcp_endpoint": "/mcp/sse"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
