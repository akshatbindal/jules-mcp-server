# Jules MCP Server

A remote Model Context Protocol (MCP) server for the Google Jules API, designed for deployment on Google Cloud Run.

## Features

This server exposes the following Jules API (v1alpha) functionality as MCP tools:

- **Sources**: List and get details of connected repositories.
- **Sessions**: Create, get, list, and delete coding sessions.
- **Plans**: Approve pending plans in a session.
- **Messaging**: Send messages and feedback to active sessions.
- **Activities**: List and get activities for a session to monitor progress.

## Prerequisites

- A Google Cloud Project.
- A Jules API Key (from [jules.google.com](https://jules.google.com/settings)).
- `gcloud` CLI installed and authenticated.

## Setup

### 1. Secret Manager

Store your Jules API Key in Google Cloud Secret Manager:

```bash
echo -n "YOUR_JULES_API_KEY" | gcloud secrets create JULES_API_KEY --data-file=-
```

Ensure the Cloud Run service account has access to this secret. By default, it uses the Compute Engine default service account:

```bash
PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding JULES_API_KEY \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 2. Deployment

You can use the provided `deploy.sh` script or run the following commands:

```bash
# Set your project ID
PROJECT_ID=$(gcloud config get-value project)

# Build the image
gcloud builds submit --tag gcr.io/$PROJECT_ID/jules-mcp-server

# Deploy to Cloud Run
gcloud run deploy jules-mcp-server \
  --image gcr.io/$PROJECT_ID/jules-mcp-server \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --set-env-vars JULES_API_KEY_SECRET_NAME=JULES_API_KEY
```

## Usage

Once deployed, the MCP endpoint will be:
`https://<your-cloud-run-url>/mcp/sse`

You can add this to your MCP client (e.g., Claude Desktop, Cursor) using the SSE transport.

### Example Configuration for Claude Desktop

```json
{
  "mcpServers": {
    "jules": {
      "url": "https://jules-mcp-server-xxxxx-xx.a.run.app/mcp/sse"
    }
  }
}
```

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export JULES_API_KEY=your_key_here
   ```

3. Run the server:
   ```bash
   python -m src.main
   ```

The server will be available at `http://localhost:8080`.
