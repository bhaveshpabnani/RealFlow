"""API routes for RealFlow CRE Agent"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from typing import Dict, Any, List
import json
from datetime import datetime

from ..services.vapi_service import VapiService
from ..services.sheets_service import GoogleSheetsService
from ..services.webhook_service import WebhookService
from ..config import settings
from ..models import VapiWebhookPayload

router = APIRouter()

# Service instances
vapi_service = VapiService()
sheets_service = GoogleSheetsService()
webhook_service = WebhookService()


@router.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic information"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RealFlow CRE Agent</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
            .info-box {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .status {{ color: #27ae60; font-weight: bold; }}
            .phone {{ font-size: 24px; color: #e74c3c; font-weight: bold; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ padding: 8px 0; border-bottom: 1px solid #eee; }}
            .endpoint {{ font-family: monospace; background: #f8f9fa; padding: 5px; border-radius: 3px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏢 RealFlow Commercial Real Estate AI Agent</h1>
            
            <div class="info-box">
                <h3>📞 Call Our AI Agent</h3>
                <p class="phone">{settings.phone_number}</p>
                <p>Our AI agent <strong>{settings.agent_name}</strong> is ready to assist with all your commercial real estate needs!</p>
            </div>
            
            <div class="info-box">
                <h3>🏢 Brokerage Information</h3>
                <p><strong>Company:</strong> {settings.brokerage_name}</p>
                <p><strong>Website:</strong> <a href="{settings.brokerage_website}" target="_blank">{settings.brokerage_website}</a></p>
                <p><strong>Agent:</strong> {settings.agent_name}</p>
            </div>
            
            <div class="info-box">
                <h3>🤖 AI Capabilities</h3>
                <ul>
                    <li>✅ Handles property owners, buyers, tenants, brokers, and lenders</li>
                    <li>✅ Qualifies leads professionally with natural conversation</li>
                    <li>✅ Powered by Cartesia Sonic 3 for expressive voice</li>
                    <li>✅ Automatically logs all call data to Google Sheets</li>
                    <li>✅ 24/7 availability for inbound calls</li>
                </ul>
            </div>
            
            <div class="info-box">
                <h3>📊 System Status</h3>
                <p class="status">🟢 System Online</p>
                <p><strong>Assistant ID:</strong> {settings.assistant_id}</p>
                <p><strong>Last Updated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="info-box">
                <h3>🔗 API Endpoints</h3>
                <ul>
                    <li><span class="endpoint">GET /health</span> - Health check</li>
                    <li><span class="endpoint">POST /webhook/vapi</span> - Vapi webhook handler</li>
                    <li><span class="endpoint">POST /assistant/create</span> - Create RealFlow assistant</li>
                    <li><span class="endpoint">POST /assistant/create-with-tools</span> - Create assistant with tools</li>
                    <li><span class="endpoint">POST /call/initiate</span> - Initiate call</li>
                    <li><span class="endpoint">GET /assistants</span> - List assistants</li>
                    <li><span class="endpoint">GET /stats</span> - Call statistics</li>
                    <li><span class="endpoint">GET /calls/recent</span> - Recent calls</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "RealFlow CRE Agent",
        "version": "1.0.0",
        "assistant_id": settings.assistant_id,
        "brokerage": settings.brokerage_name
    }


@router.post("/webhook/vapi")
async def vapi_webhook(request: Request):
    """Handle Vapi webhook events"""
    try:
        # Get raw payload
        payload = await request.json()
        
        # Log the webhook event
        print(f"📨 Webhook received: {payload.get('message', {}).get('type', 'unknown')}")
        
        # Process based on message type
        message_type = payload.get("message", {}).get("type")
        
        if message_type == "end-of-call-report":
            success = webhook_service.process_end_of_call_report(payload)
            return {"status": "success" if success else "error", "processed": True}
        
        elif message_type == "function-call":
            success = webhook_service.process_function_call(payload)
            return {"status": "success" if success else "error", "processed": True}
        
        elif message_type == "conversation-update":
            success = webhook_service.process_conversation_update(payload)
            return {"status": "success" if success else "error", "processed": True}
        
        else:
            print(f"ℹ️ Unhandled webhook type: {message_type}")
            return {"status": "ignored", "message_type": message_type}
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_call_stats():
    """Get call statistics from Google Sheets"""
    try:
        stats = sheets_service.get_call_stats()
        return {
            "status": "success",
            "data": stats,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calls/recent")
async def get_recent_calls(limit: int = 10, sheet: str = "calls"):
    """Get recent calls from Google Sheets"""
    try:
        calls = sheets_service.get_recent_calls(sheet, limit)
        return {
            "status": "success",
            "data": calls,
            "count": len(calls),
            "sheet": sheet,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistant/info")
async def get_assistant_info():
    """Get assistant information"""
    try:
        assistant = await vapi_service.get_assistant(settings.assistant_id)
        return {
            "status": "success",
            "data": assistant,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/phone-numbers")
async def list_phone_numbers():
    """List all phone numbers"""
    try:
        phone_numbers = await vapi_service.list_phone_numbers()
        return {
            "status": "success",
            "data": phone_numbers,
            "count": len(phone_numbers),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calls")
async def list_calls(limit: int = 50):
    """List recent calls from Vapi"""
    try:
        calls = await vapi_service.list_calls(limit)
        return {
            "status": "success",
            "data": calls,
            "count": len(calls),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assistant/create")
async def create_assistant():
    """Create the RealFlow CRE assistant using predefined configuration"""
    try:
        from ..tools.assistant_manager import AssistantManager
        
        assistant_manager = AssistantManager()
        assistant_config = assistant_manager.get_assistant_config()
        
        assistant = await vapi_service.create_assistant(assistant_config)
        return {
            "status": "success",
            "message": "RealFlow CRE Assistant created successfully",
            "data": assistant,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/assistant/create-with-tools")
async def create_assistant_with_tools():
    """Create the RealFlow CRE assistant with Google Sheets tools"""
    try:
        from ..tools.assistant_manager import AssistantManager
        
        assistant_manager = AssistantManager()
        
        # First create the Google Sheets tools
        print("🔧 Creating Google Sheets tools...")
        tools = await assistant_manager.create_tools()
        
        # Get tool IDs
        tool_ids = [tool.get('id') for tool in tools if tool.get('id')]
        print(f"✅ Created {len(tool_ids)} tools: {tool_ids}")
        
        # Get assistant config and add tool IDs
        assistant_config = assistant_manager.get_assistant_config()
        assistant_config["model"]["toolIds"] = tool_ids
        
        # Create the assistant
        print("🤖 Creating assistant with tools...")
        assistant = await vapi_service.create_assistant(assistant_config)
        
        return {
            "status": "success",
            "message": "RealFlow CRE Assistant created with Google Sheets tools",
            "data": {
                "assistant": assistant,
                "tools": tools,
                "tool_ids": tool_ids
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/call/initiate")
async def initiate_call(call_request: Dict[str, Any]):
    """Initiate a call using the assistant"""
    try:
        # Extract required fields
        phone_number = call_request.get("phone_number")
        if not phone_number:
            raise HTTPException(status_code=400, detail="phone_number is required")
        
        # Use configured assistant ID or provided one
        assistant_id = call_request.get("assistant_id", settings.assistant_id)
        
        # Create call configuration
        call_config = {
            "phoneNumberId": settings.vapi_phone_number_id,
            "assistantId": assistant_id,
            "customer": {
                "number": phone_number
            }
        }
        
        # Add any additional call parameters
        if "metadata" in call_request:
            call_config["metadata"] = call_request["metadata"]
        
        call = await vapi_service.create_call(call_config)
        return {
            "status": "success",
            "data": call,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/assistants")
async def list_assistants():
    """List all assistants"""
    try:
        assistants = await vapi_service.list_assistants()
        return {
            "status": "success",
            "data": assistants,
            "count": len(assistants),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/webhook")
async def test_webhook(payload: Dict[str, Any]):
    """Test webhook processing with sample data"""
    try:
        # Process the test payload
        success = webhook_service.process_end_of_call_report(payload)
        return {
            "status": "success" if success else "error",
            "message": "Test webhook processed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))