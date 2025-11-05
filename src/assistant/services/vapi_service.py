"""Vapi API service for managing assistants and calls"""

import httpx
import json
from typing import Dict, Any, Optional, List
from ..config import settings
from ..models import CallSummary


class VapiService:
    """Service for interacting with Vapi API"""
    
    def __init__(self):
        self.api_key = settings.vapi_api_key
        self.base_url = settings.vapi_base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_assistant(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new assistant"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/assistant",
                headers=self.headers,
                json=config
            )
            response.raise_for_status()
            return response.json()
    
    async def update_assistant(self, assistant_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing assistant"""
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/assistant/{assistant_id}",
                headers=self.headers,
                json=config
            )
            response.raise_for_status()
            return response.json()
    
    async def get_assistant(self, assistant_id: str) -> Dict[str, Any]:
        """Get assistant details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/assistant/{assistant_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def list_assistants(self) -> List[Dict[str, Any]]:
        """List all assistants"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/assistant",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_phone_number(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a phone number"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/phone-number",
                headers=self.headers,
                json=config
            )
            response.raise_for_status()
            return response.json()
    
    async def list_phone_numbers(self) -> List[Dict[str, Any]]:
        """List all phone numbers"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/phone-number",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def get_call(self, call_id: str) -> Dict[str, Any]:
        """Get call details"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/call/{call_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
    
    async def create_call(self, call_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create and initiate a call"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/call",
                headers=self.headers,
                json=call_config
            )
            response.raise_for_status()
            return response.json()
    
    async def list_calls(self, limit: int = 100) -> List[Dict[str, Any]]:
        """List calls"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/call",
                headers=self.headers,
                params={"limit": limit}
            )
            response.raise_for_status()
            return response.json()
    
    async def create_tool(self, tool_config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a Google Sheets tool"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tool",
                headers=self.headers,
                json=tool_config
            )
            response.raise_for_status()
            return response.json()
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """List all tools"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/tool",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()