"""Phone number management tools for Vapi"""

import asyncio
from typing import Dict, Any, List, Optional
from ..services.vapi_service import VapiService
from ..config import settings


class PhoneManager:
    """Manage Vapi phone numbers"""
    
    def __init__(self):
        self.vapi_service = VapiService()
    
    def get_phone_number_config(self, assistant_id: str, webhook_url: str) -> Dict[str, Any]:
        """Get phone number configuration"""
        return {
            "provider": "twilio",
            "number": settings.phone_number,
            "assistantId": assistant_id,
            "serverUrl": webhook_url,
            "serverUrlSecret": settings.webhook_secret
        }
    
    async def create_phone_number(self, assistant_id: str, webhook_url: str) -> Dict[str, Any]:
        """Create a phone number"""
        config = self.get_phone_number_config(assistant_id, webhook_url)
        return await self.vapi_service.create_phone_number(config)
    
    async def list_phone_numbers(self) -> List[Dict[str, Any]]:
        """List all phone numbers"""
        return await self.vapi_service.list_phone_numbers()
    
    async def find_phone_number_by_number(self, phone_number: str) -> Optional[Dict[str, Any]]:
        """Find phone number by number"""
        phone_numbers = await self.list_phone_numbers()
        for pn in phone_numbers:
            if pn.get("number") == phone_number:
                return pn
        return None
    
    async def setup_phone_number(self, assistant_id: str, webhook_url: str) -> Dict[str, Any]:
        """Setup phone number for assistant"""
        # Check if phone number already exists
        existing = await self.find_phone_number_by_number(settings.phone_number)
        
        if existing:
            print(f"📞 Phone number {settings.phone_number} already exists")
            print(f"   ID: {existing.get('id')}")
            print(f"   Assistant ID: {existing.get('assistantId')}")
            return existing
        else:
            print(f"📞 Creating phone number {settings.phone_number}")
            return await self.create_phone_number(assistant_id, webhook_url)