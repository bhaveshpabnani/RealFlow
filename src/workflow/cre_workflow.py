"""
Main workflow orchestrator for CRE voice agent operations.
"""

from typing import Dict, List, Optional, Any
import logging
import asyncio
from datetime import datetime

from .models import CRECallData, MissingDataReport, CallerCategory, CallRequest, CallResponse
from .workflow_builder import CREWorkflowBuilder
from .vapi_client import VapiClient
from .config import config

logger = logging.getLogger(__name__)


class CREWorkflow:
    """Main workflow orchestrator for CRE voice agent operations."""
    
    def __init__(self):
        self.vapi_client = VapiClient()
        self.workflow_builder = CREWorkflowBuilder(self.vapi_client)
    
    async def create_dynamic_workflow(
        self,
        caller_type: Optional[CallerCategory] = None,
        missing_fields: Optional[List[str]] = None,
        workflow_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a dynamic VAPI workflow for CRE calls.
        
        Args:
            caller_type: Optional identified caller type
            missing_fields: Optional list of missing fields to collect
            workflow_name: Optional custom workflow name
            
        Returns:
            Workflow response with ID and details
        """
        logger.info(f"Creating dynamic CRE workflow: {workflow_name}")
        
        try:
            start_time = asyncio.get_event_loop().time()
            
            # Create dynamic workflow using WorkflowBuilder
            workflow_config = await self.workflow_builder.create_dynamic_workflow(
                caller_type, missing_fields
            )
            
            # Create workflow in VAPI
            vapi_workflow = await self.vapi_client.create_workflow(workflow_config)
            
            # Record performance metrics
            creation_time = asyncio.get_event_loop().time() - start_time
            logger.info(f"Workflow created in {creation_time:.2f} seconds")
            
            return {
                "workflow_id": vapi_workflow["id"],
                "status": "created",
                "caller_type": caller_type.value if caller_type else None,
                "missing_fields": missing_fields or [],
                "created_at": datetime.utcnow().isoformat(),
                "creation_time": creation_time
            }
            
        except Exception as e:
            logger.error(f"Error creating dynamic workflow: {str(e)}")
            raise
    
    async def initiate_call(
        self,
        customer_phone: str,
        caller_type: Optional[CallerCategory] = None,
        workflow_id: Optional[str] = None,
        initial_data: Optional[CRECallData] = None
    ) -> Dict[str, Any]:
        """
        Initiate a CRE voice call.
        
        Args:
            customer_phone: Customer phone number
            caller_type: Optional identified caller type
            workflow_id: Optional existing workflow ID
            initial_data: Optional initial call data
            
        Returns:
            Call response with ID and details
        """
        logger.info(f"Initiating CRE call to {customer_phone}")
        
        try:
            # Create workflow if not provided
            if not workflow_id:
                workflow_response = await self.create_dynamic_workflow(
                    caller_type,
                    workflow_name=f"Auto-generated for {customer_phone}"
                )
                workflow_id = workflow_response["workflow_id"]
            
            # Format phone number to E.164 format
            formatted_phone = self._format_phone_number(customer_phone)
            
            # Prepare call configuration
            call_config = {
                "workflowId": workflow_id,
                "customer": {"number": formatted_phone},
                "metadata": {
                    "caller_type": caller_type.value if caller_type else None,
                    "initial_data": initial_data.to_dict() if initial_data else {},
                    "initiated_at": datetime.utcnow().isoformat()
                }
            }
            
            # Add phone number ID for outbound calls
            if config.api_settings.vapi_phone_number_id:
                call_config["phoneNumberId"] = config.api_settings.vapi_phone_number_id
                logger.info(f"Using VAPI phone number ID: {config.api_settings.vapi_phone_number_id}")
            else:
                logger.warning("No VAPI phone number ID configured")
            
            logger.info(f"Creating call with workflow ID: {workflow_id}")
            
            # Initiate call via VAPI
            call_response = await self.vapi_client.create_call(call_config)
            
            return {
                "call_id": call_response["id"],
                "workflow_id": workflow_id,
                "status": "initiated",
                "customer_phone": formatted_phone,
                "caller_type": caller_type.value if caller_type else None,
                "estimated_duration": 300,  # 5 minutes estimate
                "created_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error initiating call: {str(e)}")
            raise
    
    async def get_call_status(self, call_id: str) -> Optional[Dict[str, Any]]:
        """
        Get current call status and collected data.
        
        Args:
            call_id: VAPI call ID
            
        Returns:
            Call status response or None if not found
        """
        logger.info(f"Getting status for call: {call_id}")
        
        try:
            # Get current status from VAPI
            vapi_call = await self.vapi_client.get_call(call_id)
            
            # Extract collected data
            collected_data = self._extract_collected_data_from_vapi_response(vapi_call)
            
            return {
                "call_id": call_id,
                "status": vapi_call.get("status", "unknown"),
                "duration": vapi_call.get("duration"),
                "collected_data": collected_data,
                "error_message": vapi_call.get("error_message")
            }
            
        except Exception as e:
            logger.error(f"Error getting call status: {str(e)}")
            raise
    
    async def handle_vapi_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle VAPI webhook callbacks.
        
        Args:
            webhook_data: Webhook payload from VAPI
            
        Returns:
            Processing result
        """
        logger.info(f"Handling VAPI webhook for call: {webhook_data.get('call', {}).get('id')}")
        
        try:
            call_data = webhook_data.get("call", {})
            call_id = call_data.get("id")
            message_data = webhook_data.get("message", {})
            message_type = message_data.get("type")
            
            if message_type == "end-of-call-report":
                return await self._handle_call_completion(webhook_data)
            elif message_type == "transcript":
                return await self._handle_transcript_update(webhook_data)
            elif message_type == "function-call":
                return await self._handle_function_call(webhook_data)
            else:
                logger.info(f"Unhandled webhook message type: {message_type}")
                return {"status": "ignored", "message_type": message_type}
            
        except Exception as e:
            logger.error(f"Error handling VAPI webhook: {str(e)}")
            raise
    
    async def _handle_call_completion(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle call completion webhook."""
        call_data = webhook_data.get("call", {})
        call_id = call_data.get("id")
        
        logger.info(f"Processing call completion for: {call_id}")
        
        # Extract collected data
        collected_data = self._extract_collected_data_from_vapi_response(call_data)
        
        # Log the completion
        logger.info(f"Call {call_id} completed with {len(collected_data)} fields collected")
        
        return {
            "status": "completed",
            "call_id": call_id,
            "collected_data": collected_data,
            "duration": call_data.get("duration"),
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def _handle_transcript_update(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle transcript update webhook."""
        call_data = webhook_data.get("call", {})
        call_id = call_data.get("id")
        message_data = webhook_data.get("message", {})
        
        logger.info(f"Transcript update for call: {call_id}")
        
        return {
            "status": "transcript_updated",
            "call_id": call_id,
            "transcript": message_data.get("transcript", ""),
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def _handle_function_call(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle function call webhook (e.g., Google Sheets logging)."""
        call_data = webhook_data.get("call", {})
        call_id = call_data.get("id")
        message_data = webhook_data.get("message", {})
        
        logger.info(f"Function call for call: {call_id}")
        
        # Extract function call details
        function_call = message_data.get("functionCall", {})
        function_name = function_call.get("name")
        
        if function_name == "log_cre_call_data":
            # Handle Google Sheets logging
            return await self._handle_sheets_logging(webhook_data)
        
        return {
            "status": "function_call_processed",
            "call_id": call_id,
            "function_name": function_name,
            "processed_at": datetime.utcnow().isoformat()
        }
    
    async def _handle_sheets_logging(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Google Sheets data logging."""
        call_data = webhook_data.get("call", {})
        call_id = call_data.get("id")
        
        logger.info(f"Logging call data to Google Sheets for call: {call_id}")
        
        # Extract collected data
        collected_data = self._extract_collected_data_from_vapi_response(call_data)
        
        # Format data for Google Sheets
        sheets_data = self._format_data_for_sheets(collected_data)
        
        # Log success (actual Google Sheets integration would happen here)
        logger.info(f"Successfully formatted data for Google Sheets: {len(sheets_data)} fields")
        
        return {
            "status": "sheets_logged",
            "call_id": call_id,
            "sheets_data": sheets_data,
            "processed_at": datetime.utcnow().isoformat()
        }
    
    def _extract_collected_data_from_vapi_response(self, vapi_call: Dict[str, Any]) -> Dict[str, Any]:
        """Extract collected data from VAPI call response."""
        collected_data = {}
        
        # Extract from analysis if available
        analysis = vapi_call.get("analysis", {})
        if analysis:
            structured_data = analysis.get("structuredData", {})
            if structured_data:
                collected_data.update(structured_data)
        
        # Extract from messages if available
        messages = vapi_call.get("messages", [])
        for message in messages:
            if message.get("type") == "function-call":
                function_call = message.get("functionCall", {})
                if function_call.get("name") == "log_cre_call_data":
                    parameters = function_call.get("parameters", {})
                    collected_data.update(parameters)
        
        # Extract from artifact if available
        artifact = vapi_call.get("artifact", {})
        if artifact:
            messages_artifact = artifact.get("messages", [])
            for message in messages_artifact:
                if "variableExtractionPlan" in message:
                    extracted_vars = message.get("extractedVariables", {})
                    collected_data.update(extracted_vars)
        
        return collected_data
    
    def _format_data_for_sheets(self, collected_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format collected data for Google Sheets logging."""
        from .config import FieldMappingConfig
        
        sheets_data = {}
        mapping = FieldMappingConfig.SHEETS_MAPPING
        
        # Map basic fields
        for field, column in mapping.items():
            if field in collected_data:
                sheets_data[column] = collected_data[field]
        
        # Add timestamp
        sheets_data["Timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Handle caller-specific fields based on caller type
        caller_type = collected_data.get("caller_type")
        if caller_type == "property_owner":
            owner_mapping = FieldMappingConfig.OWNER_MAPPING
            for field, column in owner_mapping.items():
                if field in collected_data:
                    sheets_data[column] = collected_data[field]
        elif caller_type == "buyer_tenant":
            buyer_mapping = FieldMappingConfig.BUYER_TENANT_MAPPING
            for field, column in buyer_mapping.items():
                if field in collected_data:
                    sheets_data[column] = collected_data[field]
        elif caller_type == "broker":
            broker_mapping = FieldMappingConfig.BROKER_MAPPING
            for field, column in broker_mapping.items():
                if field in collected_data:
                    sheets_data[column] = collected_data[field]
        elif caller_type == "lender":
            lender_mapping = FieldMappingConfig.LENDER_MAPPING
            for field, column in lender_mapping.items():
                if field in collected_data:
                    sheets_data[column] = collected_data[field]
        
        return sheets_data
    
    def _format_phone_number(self, phone: str) -> str:
        """Format phone number to E.164 format."""
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone))
        
        # Handle US numbers
        if len(digits_only) == 10:
            return f"+1{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"
        elif phone.startswith('+'):
            return phone
        else:
            # Assume US number if unclear
            return f"+1{digits_only[-10:]}"
    
    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all CRE workflows."""
        try:
            workflows = await self.vapi_client.list_workflows()
            return workflows
        except Exception as e:
            logger.error(f"Error listing workflows: {str(e)}")
            raise
    
    async def list_calls(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List recent CRE calls."""
        try:
            calls = await self.vapi_client.list_calls(limit)
            return calls
        except Exception as e:
            logger.error(f"Error listing calls: {str(e)}")
            raise