"""Data models for RealFlow CRE Agent"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class CallerType(str, Enum):
    """Types of callers"""
    PROPERTY_OWNER = "Property Owner"
    BUYER = "Buyer"
    TENANT = "Tenant"
    BROKER = "Broker"
    LENDER = "Lender"
    GENERAL_INQUIRY = "General Inquiry"


class PropertyType(str, Enum):
    """Types of commercial properties"""
    OFFICE = "Office"
    RETAIL = "Retail"
    INDUSTRIAL = "Industrial"
    MULTIFAMILY = "Multifamily"
    LAND = "Land"
    MIXED_USE = "Mixed-Use"
    OTHER = "Other"


class TransactionType(str, Enum):
    """Types of transactions"""
    SALE = "Sale"
    PURCHASE = "Purchase"
    LEASE = "Lease"
    TENANT_REP = "Tenant Rep"
    GENERAL_INQUIRY = "General Inquiry"


class Timeline(str, Enum):
    """Transaction timelines"""
    IMMEDIATE = "Immediate"
    ONE_TO_THREE_MONTHS = "1-3 months"
    THREE_TO_SIX_MONTHS = "3-6 months"
    SIX_PLUS_MONTHS = "6+ months"
    UNKNOWN = "Unknown"


class LeadQuality(str, Enum):
    """Lead quality assessment"""
    HOT = "Hot"
    WARM = "Warm"
    COLD = "Cold"


class CallData(BaseModel):
    """Base call data model"""
    timestamp: datetime = Field(default_factory=datetime.now)
    caller_name: Optional[str] = None
    caller_type: Optional[CallerType] = None
    property_type: Optional[PropertyType] = None
    market_location: Optional[str] = None
    transaction_type: Optional[TransactionType] = None
    size_budget: Optional[str] = None
    timeline: Optional[Timeline] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    additional_notes: Optional[str] = None
    lead_quality: Optional[LeadQuality] = None
    call_duration: Optional[int] = None
    call_id: Optional[str] = None


class PropertyOwnerData(CallData):
    """Data specific to property owners"""
    property_status: Optional[str] = None  # Occupied, Vacant, Partially Occupied
    asking_price: Optional[str] = None
    current_income: Optional[str] = None
    reason_for_selling: Optional[str] = None


class BuyerTenantData(CallData):
    """Data specific to buyers and tenants"""
    budget_range: Optional[str] = None
    preferred_locations: Optional[List[str]] = None
    must_have_amenities: Optional[List[str]] = None
    current_location: Optional[str] = None
    move_reason: Optional[str] = None


class BrokerData(CallData):
    """Data specific to brokers"""
    brokerage_name: Optional[str] = None
    license_number: Optional[str] = None
    collaboration_type: Optional[str] = None  # Referral, Co-listing, etc.
    deal_details: Optional[str] = None


class VapiWebhookPayload(BaseModel):
    """Vapi webhook payload structure"""
    message: Dict[str, Any]
    call: Dict[str, Any]
    artifact: Optional[Dict[str, Any]] = None


class CallSummary(BaseModel):
    """Call summary for logging"""
    call_id: str
    phone_number: str
    duration: int
    status: str
    transcript: str
    structured_data: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)


class GoogleSheetsRow(BaseModel):
    """Google Sheets row data"""
    timestamp: str
    caller_name: str
    caller_type: str
    property_type: str
    market_location: str
    transaction_type: str
    size_budget: str
    timeline: str
    contact_phone: str
    contact_email: str
    additional_notes: str
    lead_quality: str
    call_duration: str