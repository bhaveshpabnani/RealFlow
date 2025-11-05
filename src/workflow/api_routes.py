"""
API routes for CRE workflow management.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import os

from .cre_workflow import CREWorkflow
from .models import CallerCategory, CallRequest, CallResponse, CRECallData
from .vapi_client import VapiClient
from .services.sheets_service import WorkflowSheetsService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/workflow", tags=["CRE Workflow"])

# Initialize workflow manager
cre_workflow = CREWorkflow()


@router.post("/create", response_model=Dict[str, Any])
async def create_workflow(workflow_name: Optional[str] = "RealFlow CRE Workflow"):
    """Create the predefined RealFlow CRE workflow on VAPI."""
    try:
        from .realflow_workflow_template import get_realflow_cre_workflow_template
        
        # Get the predefined RealFlow CRE workflow template
        workflow_config = get_realflow_cre_workflow_template(workflow_name)
        
        # Create the workflow on VAPI
        vapi_client = VapiClient()
        result = await vapi_client.create_workflow(workflow_config)
        
        return {
            "status": "success",
            "message": "RealFlow CRE Workflow created successfully on VAPI",
            "data": result,
            "workflow_name": workflow_name,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/call/initiate", response_model=Dict[str, Any])
async def initiate_call(
    customer_phone: str,
    workflow_id: str,
    phone_number_id: Optional[str] = None
):
    """Initiate a CRE call using the specified workflow."""
    try:
        # Create call configuration for VAPI
        call_config = {
            "workflowId": workflow_id,
            "customer": {
                "number": customer_phone
            }
        }
        
        # Add phone number ID if provided
        if phone_number_id:
            call_config["phoneNumberId"] = phone_number_id
        
        # Create the call using VAPI client
        vapi_client = VapiClient()
        result = await vapi_client.create_call(call_config)
        
        return {
            "status": "success",
            "message": "CRE call initiated successfully",
            "data": result,
            "customer_phone": customer_phone,
            "workflow_id": workflow_id,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error initiating call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/call/{call_id}/status", response_model=Dict[str, Any])
async def get_call_status(call_id: str):
    """Get call status and collected data."""
    try:
        result = await cre_workflow.get_call_status(call_id)
        if not result:
            raise HTTPException(status_code=404, detail="Call not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting call status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/vapi")
async def handle_vapi_webhook(
    webhook_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Handle VAPI webhook callbacks."""
    try:
        # Process webhook in background
        background_tasks.add_task(
            process_webhook_background,
            webhook_data
        )
        
        # Return immediate response
        return {"status": "received", "timestamp": datetime.utcnow().isoformat()}
    except Exception as e:
        logger.error(f"Error handling webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


async def process_webhook_background(webhook_data: Dict[str, Any]):
    """Process webhook data in background."""
    try:
        result = await cre_workflow.handle_vapi_webhook(webhook_data)
        logger.info(f"Webhook processed: {result.get('status')}")
    except Exception as e:
        logger.error(f"Error processing webhook in background: {str(e)}")


@router.get("/workflows", response_model=List[Dict[str, Any]])
async def list_workflows():
    """List all CRE workflows."""
    try:
        workflows = await cre_workflow.list_workflows()
        return workflows
    except Exception as e:
        logger.error(f"Error listing workflows: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calls", response_model=List[Dict[str, Any]])
async def list_calls(limit: int = 100):
    """List recent CRE calls."""
    try:
        calls = await cre_workflow.list_calls(limit)
        return calls
    except Exception as e:
        logger.error(f"Error listing calls: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/caller-types", response_model=List[str])
async def get_caller_types():
    """Get available caller types."""
    return [caller_type.value for caller_type in CallerCategory]


@router.post("/test/workflow")
async def test_workflow_creation():
    """Test workflow creation with sample data."""
    try:
        # Create a test workflow for property owners
        result = await cre_workflow.create_dynamic_workflow(
            caller_type=CallerCategory.PROPERTY_OWNER,
            missing_fields=["asking_price", "property_status"],
            workflow_name="Test Property Owner Workflow"
        )
        return {
            "status": "success",
            "message": "Test workflow created successfully",
            "workflow_data": result
        }
    except Exception as e:
        logger.error(f"Error creating test workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/call")
async def test_call_initiation(phone_number: str = "+1234567890"):
    """Test call initiation with sample data."""
    try:
        # Create a test call
        result = await cre_workflow.initiate_call(
            customer_phone=phone_number,
            caller_type=CallerCategory.PROPERTY_OWNER
        )
        return {
            "status": "success",
            "message": "Test call initiated successfully",
            "call_data": result
        }
    except Exception as e:
        logger.error(f"Error initiating test call: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def workflow_health_check():
    """Health check for workflow system."""
    try:
        # Test VAPI client connection
        vapi_client = VapiClient()
        workflows = await vapi_client.list_workflows()
        
        # Test Google Sheets connection if configured
        sheets_status = "not_configured"
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if spreadsheet_id and os.path.exists(credentials_path):
            try:
                sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
                sheets_test = sheets_service.test_connection()
                sheets_status = sheets_test["status"]
            except Exception as e:
                sheets_status = f"error: {str(e)}"
        
        return {
            "status": "healthy",
            "vapi_connection": "ok",
            "workflows_count": len(workflows),
            "sheets_connection": sheets_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Workflow health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/stats/calls")
async def get_call_statistics():
    """Get call statistics from Google Sheets."""
    try:
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if not spreadsheet_id or not os.path.exists(credentials_path):
            raise HTTPException(
                status_code=404, 
                detail="Google Sheets not configured or credentials not found"
            )
        
        sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
        stats = sheets_service.get_call_statistics()
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting call statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/recent/{sheet_name}")
async def get_recent_calls(sheet_name: str, limit: int = 10):
    """Get recent calls from specific sheet."""
    try:
        if sheet_name not in ["owner", "customer", "broker", "lender", "general"]:
            raise HTTPException(status_code=400, detail="Invalid sheet name")
        
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if not spreadsheet_id or not os.path.exists(credentials_path):
            raise HTTPException(
                status_code=404, 
                detail="Google Sheets not configured or credentials not found"
            )
        
        sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
        recent_calls = sheets_service.get_recent_calls(sheet_name, limit)
        
        return {
            "sheet_name": sheet_name,
            "calls": recent_calls,
            "count": len(recent_calls)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recent calls: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sheets/test-log")
async def test_sheets_logging():
    """Test Google Sheets logging with sample data."""
    try:
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if not spreadsheet_id or not os.path.exists(credentials_path):
            raise HTTPException(
                status_code=404, 
                detail="Google Sheets not configured or credentials not found"
            )
        
        # Sample test data
        test_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "caller_name": "John Doe (Test)",
            "caller_type": "property_owner",
            "property_type": "office",
            "property_location": "Downtown Test Area",
            "transaction_type": "sale",
            "budget_range": "$500,000 - $750,000",
            "timeline": "3_to_6_months",
            "contact_phone": "+1234567890",
            "contact_email": "test@example.com",
            "additional_notes": "Test call from workflow system",
            "lead_quality": "warm",
            "call_duration": "180",
            "property_address": "123 Test Street",
            "asking_price": "$650,000",
            "property_status": "occupied"
        }
        
        sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
        success = sheets_service.log_call_data("owner", test_data)
        
        if success:
            return {
                "status": "success",
                "message": "Test data logged successfully",
                "test_data": test_data
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to log test data")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing sheets logging: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))