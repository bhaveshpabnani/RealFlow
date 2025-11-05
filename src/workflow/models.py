"""
Data models for RealFlow CRE workflow implementation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import datetime


class CallerCategory(Enum):
    """Categories of callers for CRE workflow."""
    PROPERTY_OWNER = "property_owner"
    BUYER_TENANT = "buyer_tenant"
    BROKER = "broker"
    LENDER = "lender"
    GENERAL_INQUIRY = "general_inquiry"


class PropertyType(Enum):
    """Types of commercial properties."""
    OFFICE = "office"
    RETAIL = "retail"
    INDUSTRIAL = "industrial"
    MULTIFAMILY = "multifamily"
    LAND = "land"
    MIXED_USE = "mixed_use"
    OTHER = "other"


class TransactionType(Enum):
    """Types of real estate transactions."""
    SALE = "sale"
    PURCHASE = "purchase"
    LEASE = "lease"
    TENANT_REP = "tenant_rep"
    GENERAL_INQUIRY = "general_inquiry"


class Timeline(Enum):
    """Transaction timelines."""
    IMMEDIATE = "immediate"
    ONE_TO_THREE_MONTHS = "1_to_3_months"
    THREE_TO_SIX_MONTHS = "3_to_6_months"
    SIX_PLUS_MONTHS = "6_plus_months"
    UNKNOWN = "unknown"


class LeadQuality(Enum):
    """Lead quality assessment."""
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


@dataclass
class CRECallData:
    """Represents data collected from a CRE call."""
    # Basic information
    caller_name: Optional[str] = None
    caller_type: Optional[CallerCategory] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    
    # Property information
    property_type: Optional[PropertyType] = None
    property_location: Optional[str] = None
    property_size: Optional[str] = None
    property_address: Optional[str] = None
    
    # Transaction details
    transaction_type: Optional[TransactionType] = None
    budget_range: Optional[str] = None
    timeline: Optional[Timeline] = None
    
    # Owner-specific data
    asking_price: Optional[str] = None
    current_income: Optional[str] = None
    property_status: Optional[str] = None  # Occupied, Vacant, etc.
    reason_for_selling: Optional[str] = None
    
    # Buyer/Tenant-specific data
    preferred_locations: Optional[List[str]] = None
    must_have_amenities: Optional[List[str]] = None
    current_location: Optional[str] = None
    move_reason: Optional[str] = None
    
    # Broker-specific data
    brokerage_name: Optional[str] = None
    license_number: Optional[str] = None
    collaboration_type: Optional[str] = None
    deal_details: Optional[str] = None
    
    # Lender-specific data
    loan_types: Optional[List[str]] = None
    lending_area: Optional[str] = None
    max_loan_amount: Optional[str] = None
    
    # General
    additional_notes: Optional[str] = None
    lead_quality: Optional[LeadQuality] = None
    
    # Metadata
    call_id: Optional[str] = None
    call_duration: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        from dataclasses import asdict
        result = asdict(self)
        # Convert enums to their values
        for key, value in result.items():
            if isinstance(value, Enum):
                result[key] = value.value
            elif isinstance(value, list) and value and isinstance(value[0], Enum):
                result[key] = [item.value for item in value]
        return result


@dataclass
class MissingDataReport:
    """Report of missing information from initial call screening."""
    caller_info_missing: List[str] = field(default_factory=list)
    property_info_missing: List[str] = field(default_factory=list)
    transaction_info_missing: List[str] = field(default_factory=list)
    specific_details_missing: List[str] = field(default_factory=list)
    
    priority_order: List[CallerCategory] = field(default_factory=list)
    total_missing_count: int = 0
    
    def has_missing_data(self) -> bool:
        """Check if there is any missing data."""
        return self.total_missing_count > 0


@dataclass
class VariableExtraction:
    """Variable extraction configuration for a workflow node."""
    name: str
    type: str  # "string", "number", "boolean", "array"
    description: str
    enum: Optional[List[str]] = None
    required: bool = True


@dataclass
class ConversationNode:
    """Configuration for a conversation node in the CRE workflow."""
    id: str
    type: str = "conversation"
    name: Optional[str] = None
    prompt: str = ""
    first_message: str = ""
    model_settings: Optional[Dict[str, Any]] = None
    transcriber_settings: Optional[Dict[str, Any]] = None
    variable_extractions: List[VariableExtraction] = field(default_factory=list)
    is_global: bool = False
    condition: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ToolNode:
    """Configuration for a tool node in the CRE workflow."""
    id: str
    type: str = "tool"
    name: Optional[str] = None
    tool_type: str = "endCall"  # "endCall", "transferCall", "googleSheets"
    function_name: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)
    messages: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowEdge:
    """Configuration for an edge between workflow nodes."""
    from_node: str
    to_node: str
    condition_type: str = "ai"
    condition_prompt: str = ""


@dataclass
class WorkflowConfig:
    """Complete CRE workflow configuration."""
    name: str
    nodes: List[Union[ConversationNode, ToolNode]] = field(default_factory=list)
    edges: List[WorkflowEdge] = field(default_factory=list)
    voice_settings: Optional[Dict[str, Any]] = None
    global_prompt: str = ""
    
    def add_node(self, node: Union[ConversationNode, ToolNode]):
        """Add a node to the workflow."""
        self.nodes.append(node)
    
    def add_edge(self, edge: WorkflowEdge):
        """Add an edge to the workflow."""
        self.edges.append(edge)
    
    def get_node_by_id(self, node_id: str) -> Optional[Union[ConversationNode, ToolNode]]:
        """Get a node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None


@dataclass
class CallRequest:
    """Request to initiate a CRE workflow call."""
    customer_phone: str
    caller_type: Optional[CallerCategory] = None
    initial_data: Optional[CRECallData] = None
    workflow_id: Optional[str] = None
    call_metadata: Optional[Dict[str, Any]] = None


@dataclass
class CallResponse:
    """Response from CRE call initiation."""
    call_id: str
    workflow_id: str
    status: str
    created_at: str
    estimated_duration: Optional[int] = None