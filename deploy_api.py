import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from src.graph import Workflow
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Any, Dict

# Load .env file
load_dotenv()

app = FastAPI(
    title="Gmail Automation",
    version="1.0",
    description="LangGraph backend for the AI Gmail automation workflow",
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

# Define simple input/output models to help with schema generation
class WorkflowInput(BaseModel):
    input: Dict[str, Any]

class WorkflowOutput(BaseModel):
    output: Dict[str, Any]

def get_runnable():
    workflow = Workflow()
    # Make sure all models are rebuilt
    try:
        # Force rebuild of any Pydantic models in your workflow
        if hasattr(workflow, 'app'):
            return workflow.app
        return workflow
    except Exception as e:
        print(f"Error building workflow: {e}")
        raise

# Fetch LangGraph Automation runnable
runnable = get_runnable()

# Create the Fast API route to invoke the runnable
try:
    add_routes(
        app, 
        runnable,
        path="/gmail-automation",
        include_callback_events=False,
        enable_feedback_endpoint=False,
        input_type=Dict[str, Any],  # Specify input type
        output_type=Dict[str, Any], # Specify output type
    )
except Exception as e:
    print(f"Error adding routes: {e}")
    # Fallback: add routes with minimal configuration
    add_routes(app, runnable)

def main():
    # Start the API
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
