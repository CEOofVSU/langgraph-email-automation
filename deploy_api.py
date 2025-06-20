import uvicorn
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

app = FastAPI(
    title="Gmail Automation",
    version="1.0",
    description="LangGraph backend for the AI Gmail automation workflow",
    # Disable OpenAPI docs to avoid the schema generation error
    docs_url=None,
    redoc_url=None,
    openapi_url=None
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

def get_runnable():
    """Get the LangGraph workflow runnable"""
    try:
        workflow = Workflow()
        logger.info("Workflow created successfully")
        return workflow.app
    except Exception as e:
        logger.error(f"Error creating workflow: {e}")
        raise

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

# Fetch LangGraph Automation runnable
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
    
    @app.post("/gmail-automation/invoke")
    async def workflow_invoke_fallback():
        return {"error": "Workflow not available due to initialization error", "details": str(e)}

def main():
    # Start the API
    print("🚀 Starting Gmail Automation API...")
    print("📧 Workflow endpoint: http://localhost:8000/gmail-automation/invoke")
    print("🎮 Playground: http://localhost:8000/gmail-automation/playground")
    print("❤️ Health check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
