"""Unified main application entry point for RealFlow CRE System"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import sys

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import both routers
from workflow.api_routes import router as workflow_router
from assistant.api.routes import router as assistant_router
from workflow.config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🚀 Starting RealFlow CRE Complete System...")
    
    try:
        print(f"🔑 VAPI API Key: {'*' * (len(config.api_settings.vapi_api_key) - 4) + config.api_settings.vapi_api_key[-4:]}")
        print(f"📞 VAPI Phone Number: {config.api_settings.vapi_phone_number or 'Not configured'}")
        print(f"🎤 Voice Provider: {config.voice_settings.provider}")
        print(f"🎯 Voice ID: {config.voice_settings.voice_id}")
        print(f"🤖 Model: {config.model_settings.model}")
        
        # Test VAPI connection
        from workflow.vapi_client import VapiClient
        vapi_client = VapiClient()
        try:
            workflows = await vapi_client.list_workflows()
            print(f"✅ VAPI Connection: OK ({len(workflows)} workflows found)")
        except Exception as e:
            print(f"⚠️  VAPI Connection: Warning - {str(e)}")
        
    except Exception as e:
        print(f"⚠️  Configuration Warning: {str(e)}")
    
    yield
    print("🛑 Shutting down RealFlow CRE Complete System...")


# Create unified FastAPI app
app = FastAPI(
    title="RealFlow CRE Complete System",
    description="Unified VAPI Assistant and Workflow System for Commercial Real Estate",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include both routers
app.include_router(workflow_router)  # Prefixed with /workflow/
app.include_router(assistant_router, prefix="/assistant", tags=["Assistant"])  # Prefixed with /assistant/

# Add unified root endpoint
@app.get("/")
async def root():
    """Root endpoint with complete system information"""
    return {
        "system": "RealFlow CRE Complete System",
        "version": "1.0.0",
        "description": "Unified VAPI Assistant and Workflow System for Commercial Real Estate",
        "status": "running",
        "components": {
            "workflow_system": "Dynamic workflow creation and management",
            "assistant_system": "Direct assistant management and calls"
        },
        "endpoints": {
            "workflow": {
                "create_workflow": "/workflow/create",
                "initiate_call": "/workflow/call/initiate",
                "list_workflows": "/workflow/workflows",
                "list_calls": "/workflow/calls",
                "health": "/workflow/health"
            },
            "assistant": {
                "create_assistant": "/assistant/assistant/create",
                "initiate_call": "/assistant/call/initiate",
                "list_assistants": "/assistant/assistants",
                "list_calls": "/assistant/calls",
                "health": "/assistant/health"
            },
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "features": [
            "Dynamic workflow creation",
            "Direct assistant management",
            "Caller type identification", 
            "One question per turn",
            "Google Sheets integration",
            "Lead qualification",
            "Professional CRE voice agent",
            "Cartesia Sonic 3 voice",
            "Real-time webhook processing"
        ]
    }


@app.get("/health")
async def unified_health_check():
    """Unified health check for both systems"""
    try:
        # Test VAPI client connection
        from workflow.vapi_client import VapiClient
        vapi_client = VapiClient()
        workflows = await vapi_client.list_workflows()
        
        # Test Google Sheets connection if configured
        sheets_status = "not_configured"
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if spreadsheet_id and os.path.exists(credentials_path):
            try:
                from workflow.services.sheets_service import WorkflowSheetsService
                sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
                sheets_test = sheets_service.test_connection()
                sheets_status = sheets_test["status"]
            except Exception as e:
                sheets_status = f"error: {str(e)}"
        
        return {
            "status": "healthy",
            "systems": {
                "workflow": "ok",
                "assistant": "ok"
            },
            "vapi_connection": "ok",
            "workflows_count": len(workflows),
            "sheets_connection": sheets_status,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }


def dev():
    """Run development server"""
    print("🔧 Starting RealFlow CRE Complete System in development mode...")
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


def start():
    """Run production server"""
    print("🚀 Starting RealFlow CRE Complete System in production mode...")
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    dev()