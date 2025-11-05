"""
VAPI client for CRE workflow management.
"""

import httpx
import json
from typing import Dict, Any, Optional, List
import logging
from .config import config

logger = logging.getLogger(__name__)


class VapiClient:
    """Client for interacting with VAPI API for CRE workflows."""
    
    def __init__(self):
        self.api_key = config.api_settings.vapi_api_key
        self.base_url = config.api_settings.vapi_base_url
        self.timeout = config.api_settings.timeout
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new workflow in VAPI."""
        logger.info(f"Creating workflow: {workflow_config.get('name')}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/workflow",
                    headers=self.headers,
                    json=workflow_config
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Successfully created workflow: {result.get('id')}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating workflow: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error creating workflow: {str(e)}")
            raise
    
    async def update_workflow(self, workflow_id: str, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing workflow in VAPI."""
        logger.info(f"Updating workflow: {workflow_id}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.patch(
                    f"{self.base_url}/workflow/{workflow_id}",
                    headers=self.headers,
                    json=workflow_config
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Successfully updated workflow: {workflow_id}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error updating workflow: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error updating workflow: {str(e)}")
            raise
    
    async def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow details from VAPI."""
        logger.info(f"Getting workflow: {workflow_id}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/workflow/{workflow_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting workflow: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error getting workflow: {str(e)}")
            raise
    
    async def list_workflows(self) -> List[Dict[str, Any]]:
        """List all workflows from VAPI."""
        logger.info("Listing workflows")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/workflow",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error listing workflows: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error listing workflows: {str(e)}")
            raise
    
    async def delete_workflow(self, workflow_id: str) -> bool:
        """Delete a workflow from VAPI."""
        logger.info(f"Deleting workflow: {workflow_id}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.delete(
                    f"{self.base_url}/workflow/{workflow_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                logger.info(f"Successfully deleted workflow: {workflow_id}")
                return True
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error deleting workflow: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error deleting workflow: {str(e)}")
            raise
    
    async def create_call(self, call_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a call using a workflow."""
        logger.info(f"Creating call with workflow: {call_config.get('workflowId')}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/call",
                    headers=self.headers,
                    json=call_config
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Successfully created call: {result.get('id')}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating call: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error creating call: {str(e)}")
            raise
    
    async def get_call(self, call_id: str) -> Dict[str, Any]:
        """Get call details from VAPI."""
        logger.info(f"Getting call: {call_id}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/call/{call_id}",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error getting call: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error getting call: {str(e)}")
            raise
    
    async def list_calls(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List calls from VAPI."""
        logger.info(f"Listing calls (limit: {limit})")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/call",
                    headers=self.headers,
                    params={"limit": limit}
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error listing calls: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error listing calls: {str(e)}")
            raise
    
    async def create_tool(self, tool_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a tool (like Google Sheets integration) in VAPI."""
        logger.info(f"Creating tool: {tool_config.get('name')}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/tool",
                    headers=self.headers,
                    json=tool_config
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Successfully created tool: {result.get('id')}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating tool: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error creating tool: {str(e)}")
            raise
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all tools from VAPI."""
        logger.info("Listing tools")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/tool",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error listing tools: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error listing tools: {str(e)}")
            raise
    
    async def create_phone_number(self, phone_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a phone number in VAPI."""
        logger.info(f"Creating phone number")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/phone-number",
                    headers=self.headers,
                    json=phone_config
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Successfully created phone number: {result.get('id')}")
                return result
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating phone number: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error creating phone number: {str(e)}")
            raise
    
    async def list_phone_numbers(self) -> List[Dict[str, Any]]:
        """List all phone numbers from VAPI."""
        logger.info("Listing phone numbers")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.base_url}/phone-number",
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error listing phone numbers: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error listing phone numbers: {str(e)}")
            raise