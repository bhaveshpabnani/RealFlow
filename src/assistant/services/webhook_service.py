"""Webhook service for processing Vapi callbacks"""

import json
from typing import Dict, Any, Optional
from datetime import datetime
from ..models import CallData, CallerType, PropertyType, TransactionType, Timeline, LeadQuality
from .sheets_service import GoogleSheetsService


class WebhookService:
    """Service for processing webhook data"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
    
    def process_end_of_call_report(self, payload: Dict[str, Any]) -> bool:
        """Process end-of-call report from Vapi"""
        try:
            call_data = payload.get("call", {})
            artifact = payload.get("artifact", {})
            
            # Extract basic call information
            call_id = call_data.get("id")
            phone_number = call_data.get("customer", {}).get("number")
            duration = call_data.get("endedAt") and call_data.get("startedAt")
            
            if duration:
                started_at = datetime.fromisoformat(call_data["startedAt"].replace("Z", "+00:00"))
                ended_at = datetime.fromisoformat(call_data["endedAt"].replace("Z", "+00:00"))
                duration_seconds = int((ended_at - started_at).total_seconds())
            else:
                duration_seconds = None
            
            # Extract structured data from artifact
            structured_data = {}
            if artifact and "structuredOutput" in artifact:
                structured_data = artifact["structuredOutput"]
            
            # Create CallData object
            call_data_obj = self._create_call_data_from_structured_data(
                structured_data, call_id, duration_seconds
            )
            
            # Determine which sheet to log to based on caller type
            caller_type = call_data_obj.caller_type
            
            if caller_type == CallerType.PROPERTY_OWNER:
                success = self.sheets_service.log_property_owner_data(call_data_obj)
            elif caller_type in [CallerType.BUYER, CallerType.TENANT, CallerType.LENDER, CallerType.GENERAL_INQUIRY]:
                success = self.sheets_service.log_customer_data(call_data_obj)
            elif caller_type == CallerType.BROKER:
                success = self.sheets_service.log_broker_data(call_data_obj)
            else:
                # Default to customer sheet
                success = self.sheets_service.log_customer_data(call_data_obj)
            
            if success:
                print(f"✅ Successfully logged call {call_id} to Google Sheets")
            else:
                print(f"❌ Failed to log call {call_id} to Google Sheets")
            
            return success
            
        except Exception as e:
            print(f"❌ Error processing end-of-call report: {e}")
            return False
    
    def _create_call_data_from_structured_data(
        self, 
        structured_data: Dict[str, Any], 
        call_id: str, 
        duration: Optional[int]
    ) -> CallData:
        """Create CallData object from structured data"""
        
        # Parse timestamp
        timestamp_str = structured_data.get("timestamp")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            except:
                timestamp = datetime.now()
        else:
            timestamp = datetime.now()
        
        # Parse enums safely
        caller_type = None
        if structured_data.get("caller_type"):
            try:
                caller_type = CallerType(structured_data["caller_type"])
            except ValueError:
                pass
        
        property_type = None
        if structured_data.get("property_type"):
            try:
                property_type = PropertyType(structured_data["property_type"])
            except ValueError:
                pass
        
        transaction_type = None
        if structured_data.get("transaction_type"):
            try:
                transaction_type = TransactionType(structured_data["transaction_type"])
            except ValueError:
                pass
        
        timeline = None
        if structured_data.get("timeline"):
            try:
                timeline = Timeline(structured_data["timeline"])
            except ValueError:
                pass
        
        lead_quality = None
        if structured_data.get("lead_quality"):
            try:
                lead_quality = LeadQuality(structured_data["lead_quality"])
            except ValueError:
                pass
        
        return CallData(
            timestamp=timestamp,
            caller_name=structured_data.get("caller_name"),
            caller_type=caller_type,
            property_type=property_type,
            market_location=structured_data.get("market_location"),
            transaction_type=transaction_type,
            size_budget=structured_data.get("size_budget"),
            timeline=timeline,
            contact_phone=structured_data.get("contact_phone"),
            contact_email=structured_data.get("contact_email"),
            additional_notes=structured_data.get("additional_notes"),
            lead_quality=lead_quality,
            call_duration=duration,
            call_id=call_id
        )
    
    def process_function_call(self, payload: Dict[str, Any]) -> bool:
        """Process function call webhook"""
        try:
            # This would handle real-time function calls during the conversation
            # For now, we'll just log the event
            print(f"📞 Function call received: {payload.get('message', {}).get('type')}")
            return True
        except Exception as e:
            print(f"❌ Error processing function call: {e}")
            return False
    
    def process_conversation_update(self, payload: Dict[str, Any]) -> bool:
        """Process conversation update webhook"""
        try:
            # This would handle real-time conversation updates
            # For now, we'll just log the event
            print(f"💬 Conversation update received")
            return True
        except Exception as e:
            print(f"❌ Error processing conversation update: {e}")
            return False