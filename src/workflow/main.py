"""Main application entry point for RealFlow CRE Workflow System"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import config
from .api_routes import router

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🚀 Starting RealFlow CRE Workflow System...")
    
    try:
        print(f"🔑 VAPI API Key: {'*' * (len(config.api_settings.vapi_api_key) - 4) + config.api_settings.vapi_api_key[-4:]}")
        print(f"📞 VAPI Phone Number: {config.api_settings.vapi_phone_number or 'Not configured'}")
        print(f"🎤 Voice Provider: {config.voice_settings.provider}")
        print(f"🎯 Voice ID: {config.voice_settings.voice_id}")
        print(f"🤖 Model: {config.model_settings.model}")
        print(f"📊 Collection Categories: {len(config.get_collection_priority_order())}")
        
        # Test VAPI connection
        from .vapi_client import VapiClient
        vapi_client = VapiClient()
        try:
            workflows = await vapi_client.list_workflows()
            print(f"✅ VAPI Connection: OK ({len(workflows)} workflows found)")
        except Exception as e:
            print(f"⚠️  VAPI Connection: Warning - {str(e)}")
        
    except Exception as e:
        print(f"⚠️  Configuration Warning: {str(e)}")
    
    yield
    print("🛑 Shutting down RealFlow CRE Workflow System...")


# Create FastAPI app
app = FastAPI(
    title="RealFlow CRE Workflow System",
    description="Dynamic VAPI Workflow System for Commercial Real Estate Lead Generation",
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

# Include workflow routes
app.include_router(router)

# Add root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "system": "RealFlow CRE Workflow System",
        "version": "1.0.0",
        "description": "Dynamic VAPI Workflow System for Commercial Real Estate",
        "status": "running",
        "endpoints": {
            "create_workflow": "/workflow/create",
            "initiate_call": "/workflow/call/initiate",
            "list_workflows": "/workflow/workflows",
            "list_calls": "/workflow/calls",
            "health": "/workflow/health",
            "docs": "/docs",
            "openapi": "/openapi.json"
        },
        "features": [
            "Dynamic workflow creation",
            "Caller type identification", 
            "One question per turn",
            "Google Sheets integration",
            "Lead qualification",
            "Professional CRE voice agent"
        ]
    }


def dev():
    """Run development server"""
    print("🔧 Starting RealFlow CRE Workflow System in development mode...")
    uvicorn.run(
        "workflow.main:app",
        host="0.0.0.0",
        port=8001,  # Different port from assistant
        reload=True,
        log_level="info"
    )


def start():
    """Run production server"""
    print("🚀 Starting RealFlow CRE Workflow System in production mode...")
    uvicorn.run(
        "workflow.main:app",
        host="0.0.0.0",
        port=8001,  # Different port from assistant
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    dev()