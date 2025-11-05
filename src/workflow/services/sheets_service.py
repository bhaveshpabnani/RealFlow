"""Google Sheets service for CRE workflow system"""

import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class WorkflowSheetsService:
    """Google Sheets service for workflow data logging"""
    
    def __init__(self, credentials_path: str, spreadsheet_id: str):
        self.credentials_path = credentials_path
        self.spreadsheet_id = spreadsheet_id
        self.client = None
        self.spreadsheet = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, scope
            )
            
            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            logger.info(f"✅ Connected to Google Sheets: {self.spreadsheet.title}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Google Sheets: {str(e)}")
            raise
    
    def log_call_data(self, sheet_name: str, call_data: Dict[str, Any]) -> bool:
        """
        Log call data to specified sheet.
        
        Args:
            sheet_name: Name of the sheet (buyer, owner, broker)
            call_data: Dictionary containing call data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get or create worksheet
            try:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            except gspread.WorksheetNotFound:
                worksheet = self.spreadsheet.add_worksheet(
                    title=sheet_name, 
                    rows=1000, 
                    cols=25
                )
                # Add headers
                headers = self._get_headers_for_sheet(sheet_name)
                worksheet.append_row(headers)
            
            # Prepare row data
            row_data = self._prepare_row_data(call_data, sheet_name)
            
            # Append row
            worksheet.append_row(row_data)
            
            logger.info(f"✅ Logged call data to sheet: {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to log call data to {sheet_name}: {str(e)}")
            return False
    
    def log_cre_buyer_data(self, **kwargs) -> Dict[str, Any]:
        """Log buyer/tenant data to Google Sheets (VAPI function)"""
        try:
            call_data = {
                "timestamp": kwargs.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "caller_name": kwargs.get("caller_name", ""),
                "caller_type": kwargs.get("caller_type", "buyer_tenant"),
                "property_type": kwargs.get("property_type", ""),
                "market_location": kwargs.get("market_location", ""),
                "transaction_type": "purchase/lease",
                "size_budget": kwargs.get("size_budget", ""),
                "timeline": kwargs.get("timeline", ""),
                "contact_phone": kwargs.get("contact_phone", ""),
                "contact_email": kwargs.get("contact_email", ""),
                "additional_notes": kwargs.get("additional_notes", ""),
                "lead_quality": kwargs.get("lead_quality", "qualified"),
                "call_duration": kwargs.get("call_duration", ""),
                "call_id": kwargs.get("call_id", ""),
                # Buyer-specific fields
                "preferred_locations": kwargs.get("preferred_locations", ""),
                "size_requirements": kwargs.get("size_requirements", ""),
                "budget_range": kwargs.get("budget_range", "")
            }
            
            success = self.log_call_data("buyer", call_data)
            
            return {
                "success": success,
                "message": "Buyer data logged successfully" if success else "Failed to log buyer data",
                "sheet": "buyer"
            }
            
        except Exception as e:
            logger.error(f"Error in log_cre_buyer_data: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def log_cre_owner_data(self, **kwargs) -> Dict[str, Any]:
        """Log property owner data to Google Sheets (VAPI function)"""
        try:
            call_data = {
                "timestamp": kwargs.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "caller_name": kwargs.get("caller_name", ""),
                "caller_type": kwargs.get("caller_type", "property_owner"),
                "property_type": kwargs.get("property_type", ""),
                "market_location": kwargs.get("property_address", ""),
                "transaction_type": "sale",
                "size_budget": kwargs.get("asking_price", ""),
                "timeline": kwargs.get("timeline", ""),
                "contact_phone": kwargs.get("contact_phone", ""),
                "contact_email": kwargs.get("contact_email", ""),
                "additional_notes": kwargs.get("additional_notes", ""),
                "lead_quality": kwargs.get("lead_quality", "qualified"),
                "call_duration": kwargs.get("call_duration", ""),
                "call_id": kwargs.get("call_id", ""),
                # Owner-specific fields
                "property_address": kwargs.get("property_address", ""),
                "property_size": kwargs.get("property_size", ""),
                "asking_price": kwargs.get("asking_price", ""),
                "property_status": kwargs.get("property_status", "")
            }
            
            success = self.log_call_data("owner", call_data)
            
            return {
                "success": success,
                "message": "Owner data logged successfully" if success else "Failed to log owner data",
                "sheet": "owner"
            }
            
        except Exception as e:
            logger.error(f"Error in log_cre_owner_data: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def log_cre_broker_data(self, **kwargs) -> Dict[str, Any]:
        """Log broker collaboration data to Google Sheets (VAPI function)"""
        try:
            call_data = {
                "timestamp": kwargs.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                "caller_name": kwargs.get("caller_name", ""),
                "caller_type": kwargs.get("caller_type", "broker"),
                "property_type": "collaboration",
                "market_location": kwargs.get("deal_details", ""),
                "transaction_type": kwargs.get("collaboration_type", ""),
                "size_budget": "",
                "timeline": "",
                "contact_phone": kwargs.get("contact_phone", ""),
                "contact_email": kwargs.get("contact_email", ""),
                "additional_notes": kwargs.get("additional_notes", ""),
                "lead_quality": kwargs.get("lead_quality", "qualified"),
                "call_duration": kwargs.get("call_duration", ""),
                "call_id": kwargs.get("call_id", ""),
                # Broker-specific fields
                "brokerage_name": kwargs.get("brokerage_name", ""),
                "license_number": kwargs.get("license_number", ""),
                "collaboration_type": kwargs.get("collaboration_type", ""),
                "deal_details": kwargs.get("deal_details", "")
            }
            
            success = self.log_call_data("broker", call_data)
            
            return {
                "success": success,
                "message": "Broker data logged successfully" if success else "Failed to log broker data",
                "sheet": "broker"
            }
            
        except Exception as e:
            logger.error(f"Error in log_cre_broker_data: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _get_headers_for_sheet(self, sheet_name: str) -> List[str]:
        """Get appropriate headers for each sheet type"""
        
        base_headers = [
            "Timestamp", "Caller Name", "Caller Type", "Property Type",
            "Market Location", "Transaction Type", "Size/Budget", "Timeline",
            "Contact Phone", "Contact Email", "Additional Notes", 
            "Lead Quality", "Call Duration", "Call ID"
        ]
        
        if sheet_name == "buyer":
            return base_headers + [
                "Preferred Locations", "Size Requirements", "Budget Range"
            ]
        elif sheet_name == "owner":
            return base_headers + [
                "Property Address", "Property Size", "Asking Price", "Property Status"
            ]
        elif sheet_name == "broker":
            return base_headers + [
                "Brokerage Name", "License Number", "Collaboration Type", "Deal Details"
            ]
        else:  # fallback
            return base_headers
    
    def _prepare_row_data(self, call_data: Dict[str, Any], sheet_name: str) -> List[str]:
        """Prepare row data for insertion"""
        
        # Base data that all sheets have
        base_data = [
            call_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            call_data.get("caller_name", ""),
            call_data.get("caller_type", ""),
            call_data.get("property_type", ""),
            call_data.get("market_location", ""),
            call_data.get("transaction_type", ""),
            call_data.get("size_budget", ""),
            call_data.get("timeline", ""),
            call_data.get("contact_phone", ""),
            call_data.get("contact_email", ""),
            call_data.get("additional_notes", ""),
            call_data.get("lead_quality", ""),
            str(call_data.get("call_duration", "")),
            call_data.get("call_id", "")
        ]
        
        # Add sheet-specific data
        if sheet_name == "buyer":
            base_data.extend([
                call_data.get("preferred_locations", ""),
                call_data.get("size_requirements", ""),
                call_data.get("budget_range", "")
            ])
        elif sheet_name == "owner":
            base_data.extend([
                call_data.get("property_address", ""),
                call_data.get("property_size", ""),
                call_data.get("asking_price", ""),
                call_data.get("property_status", "")
            ])
        elif sheet_name == "broker":
            base_data.extend([
                call_data.get("brokerage_name", ""),
                call_data.get("license_number", ""),
                call_data.get("collaboration_type", ""),
                call_data.get("deal_details", "")
            ])
        
        return base_data
    
    def _list_to_string(self, data: Any) -> str:
        """Convert list to comma-separated string"""
        if isinstance(data, list):
            return ", ".join(str(item) for item in data)
        return str(data) if data else ""
    
    def get_recent_calls(self, sheet_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent calls from specified sheet"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            records = worksheet.get_all_records()
            
            # Return most recent calls (last N records)
            return records[-limit:] if len(records) > limit else records
            
        except Exception as e:
            logger.error(f"Failed to get recent calls from {sheet_name}: {str(e)}")
            return []
    
    def get_call_statistics(self) -> Dict[str, Any]:
        """Get call statistics across all sheets"""
        try:
            stats = {
                "total_calls": 0,
                "calls_by_type": {},
                "recent_activity": []
            }
            
            sheet_names = ["buyer", "owner", "broker"]
            
            for sheet_name in sheet_names:
                try:
                    worksheet = self.spreadsheet.worksheet(sheet_name)
                    records = worksheet.get_all_records()
                    
                    count = len(records)
                    stats["total_calls"] += count
                    stats["calls_by_type"][sheet_name] = count
                    
                    # Add recent calls to activity
                    if records:
                        recent = records[-5:]  # Last 5 calls
                        for record in recent:
                            record["sheet_type"] = sheet_name
                            stats["recent_activity"].append(record)
                
                except gspread.WorksheetNotFound:
                    stats["calls_by_type"][sheet_name] = 0
            
            # Sort recent activity by timestamp
            stats["recent_activity"].sort(
                key=lambda x: x.get("Timestamp", ""), 
                reverse=True
            )
            stats["recent_activity"] = stats["recent_activity"][:10]  # Top 10
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get call statistics: {str(e)}")
            return {"error": str(e)}
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Google Sheets connection"""
        try:
            title = self.spreadsheet.title
            worksheets = [ws.title for ws in self.spreadsheet.worksheets()]
            
            return {
                "status": "connected",
                "spreadsheet_title": title,
                "worksheets": worksheets,
                "worksheet_count": len(worksheets)
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }