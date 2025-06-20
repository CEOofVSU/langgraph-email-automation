import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.graph import Workflow
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

# Create the FastAPI app FIRST - this ensures 'app' is always available
app = FastAPI(
    title="Gmail Automation",
    version="1.0",
    description="LangGraph backend for the AI Gmail automation workflow"
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Create a simple health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Gmail Automation API is running!",
        "status": "healthy",
        "endpoints": {
            "workflow": "/gmail-automation/invoke",
            "playground": "/gmail-automation/playground",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Gmail Automation API"}

def get_runnable():
    """Get the LangGraph workflow runnable"""
    try:
        workflow = Workflow()
        logger.info("Workflow created successfully")
        return workflow.app
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise

# Initialize the workflow and routes
try:
    runnable = get_runnable()
    logger.info("Runnable obtained successfully")
    
    # Create the Fast API route to invoke the runnable
    add_routes(
        app, 
        runnable,
        path="/gmail-automation",
        include_callback_events=False,
        enable_feedback_endpoint=False,
    )
    logger.info("Routes added successfully")
    
except Exception as e:
    logger.error(f"Error setting up routes: {e}")
    
    # Add a fallback endpoint if workflow initialization fails
    @app.post("/gmail-automation/invoke")
    async def workflow_invoke_fallback():
        return {"error": "Workflow not available due to initialization error", "details": str(e)}

def main():
    # Get port from environment variable (Render sets this automatically)
    port = int(os.environ.get("PORT", 8000))
    
    # Start the API
    print("🚀 Starting Gmail Automation API...")
    print(f"📧 Workflow endpoint: /gmail-automation/invoke")
    print(f"🎮 Playground: /gmail-automation/playground")
    print(f"❤️ Health check: /health")
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

# This allows uvicorn to find the app directly
# For when Render runs: uvicorn deploy_api:app --host 0.0.0.0 --port $PORT
