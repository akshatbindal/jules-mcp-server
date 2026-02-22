#!/bin/bash

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="jules-mcp-server"
REGION="us-central1"
SECRET_NAME="JULES_API_KEY"

echo "Deploying $SERVICE_NAME to $REGION in project $PROJECT_ID..."

# Build and push the image using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Deploy to Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GOOGLE_CLOUD_PROJECT=$PROJECT_ID \
  --set-env-vars JULES_API_KEY_SECRET_NAME=$SECRET_NAME

echo "Deployment complete!"
echo "Your MCP endpoint is: $(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')/mcp/sse"
