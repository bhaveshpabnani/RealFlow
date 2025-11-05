"""Google Sheets service for logging call data"""

import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from ..config import settings
from ..models import CallData, GoogleSheetsRow


class GoogleSheetsService:
    """Service for interacting with Google Sheets"""
    
    def __init__(self):
        self.spreadsheet_id = settings.google_sheets_spreadsheet_id
        self.credentials_file = settings.google_sheets_credentials_file
        self.client = None
        self.spreadsheet = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client"""
        try:
            if os.path.exists(self.credentials_file):
                # Use service account credentials
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ]
                
                creds = Credentials.from_service_account_file(
                    self.credentials_file, 
                    scopes=scope
                )
                self.client = gspread.authorize(creds)
                self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
                print(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            else:
                print(f"⚠️ Credentials file not found: {self.credentials_file}")
        except Exception as e:
            print(f"❌ Error initializing Google Sheets client: {e}")
    
    def _get_or_create_worksheet(self, sheet_name: str) -> Optional[gspread.Worksheet]:
        """Get or create a worksheet"""
        try:
            if not self.spreadsheet:
                return None
                
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except gspread.WorksheetNotFound:
                # Create new worksheet
                worksheet = self.spreadsheet.add_worksheet(
                    title=sheet_name, 
                    rows=1000, 
                    cols=20
                )
                # Add headers
                headers = [
                    "Timestamp", "Caller Name", "Caller Type", "Property Type",
                    "Market Location", "Transaction Type", "Size/Budget", "Timeline",
                    "Contact Phone", "Contact Email", "Additional Notes", 
                    "Lead Quality", "Call Duration", "Call ID"
                ]
                worksheet.append_row(headers)
                print(f"✅ Created new worksheet: {sheet_name}")
            
            return worksheet
        except Exception as e:
            print(f"❌ Error getting/creating worksheet {sheet_name}: {e}")
            return None
    
    def log_call_data(self, call_data: CallData, sheet_name: str = "calls") -> bool:
        """Log call data to Google Sheets"""
        try:
            worksheet = self._get_or_create_worksheet(sheet_name)
            if not worksheet:
                return False
            
            # Convert call data to row format
            row_data = [
                call_data.timestamp.strftime("%Y-%m-%d %H:%M:%S") if call_data.timestamp else "",
                call_data.caller_name or "",
                call_data.caller_type.value if call_data.caller_type else "",
                call_data.property_type.value if call_data.property_type else "",
                call_data.market_location or "",
                call_data.transaction_type.value if call_data.transaction_type else "",
                call_data.size_budget or "",
                call_data.timeline.value if call_data.timeline else "",
                call_data.contact_phone or "",
                call_data.contact_email or "",
                call_data.additional_notes or "",
                call_data.lead_quality.value if call_data.lead_quality else "",
                str(call_data.call_duration) if call_data.call_duration else "",
                call_data.call_id or ""
            ]
            
            worksheet.append_row(row_data)
            print(f"✅ Logged call data to {sheet_name} sheet")
            return True
            
        except Exception as e:
            print(f"❌ Error logging call data: {e}")
            return False
    
    def log_property_owner_data(self, call_data: CallData) -> bool:
        """Log property owner specific data"""
        return self.log_call_data(call_data, "owner")
    
    def log_customer_data(self, call_data: CallData) -> bool:
        """Log customer/buyer/tenant data"""
        return self.log_call_data(call_data, "customer")
    
    def log_broker_data(self, call_data: CallData) -> bool:
        """Log broker specific data"""
        return self.log_call_data(call_data, "broker")
    
    def get_recent_calls(self, sheet_name: str = "calls", limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent calls from Google Sheets"""
        try:
            worksheet = self._get_or_create_worksheet(sheet_name)
            if not worksheet:
                return []
            
            # Get all records
            records = worksheet.get_all_records()
            
            # Return most recent calls
            return records[-limit:] if records else []
            
        except Exception as e:
            print(f"❌ Error getting recent calls: {e}")
            return []
    
    def get_call_stats(self) -> Dict[str, Any]:
        """Get call statistics"""
        try:
            stats = {
                "total_calls": 0,
                "calls_by_type": {},
                "calls_by_property_type": {},
                "recent_calls": []
            }
            
            # Get data from all sheets
            for sheet_name in ["calls", "owner", "customer", "broker"]:
                try:
                    worksheet = self.spreadsheet.worksheet(sheet_name)
                    records = worksheet.get_all_records()
                    stats["total_calls"] += len(records)
                    
                    # Count by caller type
                    for record in records:
                        caller_type = record.get("Caller Type", "Unknown")
                        stats["calls_by_type"][caller_type] = stats["calls_by_type"].get(caller_type, 0) + 1
                        
                        property_type = record.get("Property Type", "Unknown")
                        stats["calls_by_property_type"][property_type] = stats["calls_by_property_type"].get(property_type, 0) + 1
                    
                    # Add recent calls
                    stats["recent_calls"].extend(records[-5:])
                    
                except gspread.WorksheetNotFound:
                    continue
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting call stats: {e}")
            return {"error": str(e)}