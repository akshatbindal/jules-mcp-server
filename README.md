# Jules MCP Server

A remote Model Context Protocol (MCP) server for the Google Jules API, designed for deployment on Google Cloud Run.

## Tools

This server exposes the following Jules API (v1alpha) functionality as MCP tools:

### Sources
- `list_sources()`: Lists all available sources (repositories) connected to Jules.
- `get_source(source_name)`: Gets details of a single source. `source_name` should be the full resource name, e.g., `sources/github/owner/repo`.

### Sessions
- `list_sessions(page_size, page_token)`: Lists all coding sessions.
- `create_session(source, instruction, branch, require_plan_approval, auto_pr)`: Creates a new coding session.
    - `source`: Full resource name of the source.
    - `instruction`: The task for Jules to perform.
    - `branch`: The branch to work on (defaults to main).
    - `require_plan_approval`: If true, Jules will wait for plan approval before proceeding.
    - `auto_pr`: If true, Jules will automatically create a Pull Request upon completion.
- `get_session(session_name)`: Gets a single session's details and status. `session_name` should be the full resource name, e.g., `sessions/12345`.
- `delete_session(session_name)`: Deletes a session.

### Plans & Interaction
- `approve_plan(session_name)`: Approves a pending plan in a session.
- `send_message(session_name, prompt)`: Sends a message or feedback to an active session. Useful for guiding Jules or answering its questions.

### Monitoring
- `list_activities(session_name, page_size, page_token)`: Lists activities for a session to monitor progress. Activities include plan generation, code changes, and messages.
- `get_activity(activity_name)`: Gets a single activity's details. `activity_name` should be the full resource name, e.g., `sessions/12345/activities/67890`.

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
