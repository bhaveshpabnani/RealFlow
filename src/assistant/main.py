"""Main application entry point for RealFlow CRE Agent"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    print("🚀 Starting RealFlow CRE Agent...")
    print(f"📞 Phone Number: {settings.phone_number}")
    print(f"🏢 Brokerage: {settings.brokerage_name}")
    print(f"🤖 Assistant ID: {settings.assistant_id}")
    print(f"📊 Google Sheets ID: {settings.google_sheets_spreadsheet_id}")
    yield
    print("🛑 Shutting down RealFlow CRE Agent...")


# Create FastAPI app
app = FastAPI(
    title="RealFlow CRE Agent",
    description="Commercial Real Estate AI Agent using Vapi and Cartesia Sonic 3",
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

# Include routes
app.include_router(router)


def dev():
    """Run development server"""
    uvicorn.run(
        "assistant.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level="info"
    )


def start():
    """Run production server"""
    uvicorn.run(
        "assistant.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    dev()