"""
Setup tools for CRE workflow Google Sheets integration.
"""

import json
from typing import Dict, Any, List, Optional
import logging
from .vapi_client import VapiClient
from .config import config

logger = logging.getLogger(__name__)


class CREWorkflowSetup:
    """Setup tools for CRE workflow integration."""
    
    def __init__(self):
        self.vapi_client = VapiClient()
    
    async def setup_google_sheets_tools(
        self, 
        spreadsheet_id: str,
        credentials_path: str = "credentials.json"
    ) -> Dict[str, str]:
        """
        Set up Google Sheets tools for different caller types.
        
        Args:
            spreadsheet_id: Google Sheets spreadsheet ID
            credentials_path: Path to Google service account credentials
            
        Returns:
            Dictionary mapping caller types to tool IDs
        """
        logger.info("Setting up Google Sheets tools for CRE workflow")
        
        tool_ids = {}
        
        # Load credentials
        try:
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
        except FileNotFoundError:
            logger.error(f"Credentials file not found: {credentials_path}")
            raise
        
        # Define sheet configurations for different caller types
        sheet_configs = {
            "owner": {
                "name": "Property Owner Tool",
                "sheet_name": "owner",
                "description": "Log property owner call data to Google Sheets"
            },
            "customer": {
                "name": "Buyer/Tenant Tool", 
                "sheet_name": "customer",
                "description": "Log buyer/tenant call data to Google Sheets"
            },
            "broker": {
                "name": "Broker Tool",
                "sheet_name": "broker", 
                "description": "Log broker call data to Google Sheets"
            },
            "lender": {
                "name": "Lender Tool",
                "sheet_name": "lender",
                "description": "Log lender call data to Google Sheets"
            },
            "general": {
                "name": "General Inquiry Tool",
                "sheet_name": "general",
                "description": "Log general inquiry call data to Google Sheets"
            }
        }
        
        # Create tools for each caller type
        for caller_type, config_data in sheet_configs.items():
            try:
                tool_config = self._create_sheets_tool_config(
                    name=config_data["name"],
                    description=config_data["description"],
                    spreadsheet_id=spreadsheet_id,
                    sheet_name=config_data["sheet_name"],
                    credentials=credentials
                )
                
                tool_response = await self.vapi_client.create_tool(tool_config)
                tool_ids[caller_type] = tool_response["id"]
                
                logger.info(f"Created {caller_type} tool: {tool_response['id']}")
                
            except Exception as e:
                logger.error(f"Error creating {caller_type} tool: {str(e)}")
                raise
        
        logger.info(f"Successfully created {len(tool_ids)} Google Sheets tools")
        return tool_ids
    
    def _create_sheets_tool_config(
        self,
        name: str,
        description: str,
        spreadsheet_id: str,
        sheet_name: str,
        credentials: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create Google Sheets tool configuration."""
        
        return {
            "type": "gsheet",
            "name": name,
            "description": description,
            "gsheetConfig": {
                "spreadsheetId": spreadsheet_id,
                "sheetName": sheet_name,
                "credentials": {
                    "type": credentials["type"],
                    "project_id": credentials["project_id"],
                    "private_key_id": credentials["private_key_id"],
                    "private_key": credentials["private_key"],
                    "client_email": credentials["client_email"],
                    "client_id": credentials["client_id"],
                    "auth_uri": credentials["auth_uri"],
                    "token_uri": credentials["token_uri"],
                    "auth_provider_x509_cert_url": credentials["auth_provider_x509_cert_url"],
                    "client_x509_cert_url": credentials["client_x509_cert_url"]
                }
            }
        }
    
    async def setup_phone_number(
        self,
        phone_number: str,
        workflow_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Set up phone number for CRE workflow.
        
        Args:
            phone_number: Phone number to configure
            workflow_id: Optional workflow ID to associate
            
        Returns:
            Phone number configuration response
        """
        logger.info(f"Setting up phone number: {phone_number}")
        
        try:
            phone_config = {
                "provider": "twilio",
                "number": phone_number,
                "name": f"CRE Workflow Phone - {phone_number}"
            }
            
            if workflow_id:
                phone_config["workflowId"] = workflow_id
            
            phone_response = await self.vapi_client.create_phone_number(phone_config)
            
            logger.info(f"Successfully configured phone number: {phone_response['id']}")
            return phone_response
            
        except Exception as e:
            logger.error(f"Error setting up phone number: {str(e)}")
            raise
    
    async def create_default_workflow(self) -> Dict[str, Any]:
        """Create a default CRE workflow for general use."""
        logger.info("Creating default CRE workflow")
        
        try:
            from .cre_workflow import CREWorkflow
            
            workflow_manager = CREWorkflow()
            result = await workflow_manager.create_dynamic_workflow(
                workflow_name="Default CRE Workflow"
            )
            
            logger.info(f"Created default workflow: {result['workflow_id']}")
            return result
            
        except Exception as e:
            logger.error(f"Error creating default workflow: {str(e)}")
            raise
    
    async def setup_complete_system(
        self,
        spreadsheet_id: str,
        phone_number: str,
        credentials_path: str = "credentials.json"
    ) -> Dict[str, Any]:
        """
        Set up complete CRE workflow system.
        
        Args:
            spreadsheet_id: Google Sheets spreadsheet ID
            phone_number: Phone number to configure
            credentials_path: Path to Google service account credentials
            
        Returns:
            Complete setup response
        """
        logger.info("Setting up complete CRE workflow system")
        
        try:
            # Create Google Sheets tools
            tool_ids = await self.setup_google_sheets_tools(
                spreadsheet_id, credentials_path
            )
            
            # Create default workflow
            workflow_result = await self.create_default_workflow()
            workflow_id = workflow_result["workflow_id"]
            
            # Set up phone number
            phone_result = await self.setup_phone_number(
                phone_number, workflow_id
            )
            
            setup_result = {
                "status": "complete",
                "workflow_id": workflow_id,
                "phone_number_id": phone_result["id"],
                "tool_ids": tool_ids,
                "spreadsheet_id": spreadsheet_id,
                "phone_number": phone_number
            }
            
            logger.info("CRE workflow system setup completed successfully")
            return setup_result
            
        except Exception as e:
            logger.error(f"Error setting up complete system: {str(e)}")
            raise
    
    async def list_existing_tools(self) -> List[Dict[str, Any]]:
        """List existing VAPI tools."""
        try:
            tools = await self.vapi_client.list_tools()
            return tools
        except Exception as e:
            logger.error(f"Error listing tools: {str(e)}")
            raise
    
    async def list_existing_workflows(self) -> List[Dict[str, Any]]:
        """List existing VAPI workflows."""
        try:
            workflows = await self.vapi_client.list_workflows()
            return workflows
        except Exception as e:
            logger.error(f"Error listing workflows: {str(e)}")
            raise
    
    async def list_existing_phone_numbers(self) -> List[Dict[str, Any]]:
        """List existing VAPI phone numbers."""
        try:
            phone_numbers = await self.vapi_client.list_phone_numbers()
            return phone_numbers
        except Exception as e:
            logger.error(f"Error listing phone numbers: {str(e)}")
            raise