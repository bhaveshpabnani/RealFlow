"""
Factory for creating dynamic VAPI workflow nodes for CRE agent.
"""

from typing import Dict, List, Optional, Any
import logging
from .models import ConversationNode, ToolNode, VariableExtraction, CallerCategory
from .config import InformationCategory, config

logger = logging.getLogger(__name__)


class CRENodeFactory:
    """Factory for creating different types of CRE workflow nodes."""
    
    def __init__(self):
        pass
    
    def create_introduction_node(self) -> ConversationNode:
        """Create the introduction node with caller type identification."""
        return ConversationNode(
            id="introduction",
            name="Introduction and Caller Type Identification",
            prompt=self._get_introduction_prompt(),
            first_message=self._get_introduction_first_message(),
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=[
                VariableExtraction(
                    name="caller_name",
                    type="string",
                    description="The caller's name",
                    required=False
                ),
                VariableExtraction(
                    name="caller_type",
                    type="string",
                    description="Type of caller (property owner, buyer, tenant, broker, lender, general inquiry)",
                    enum=["property_owner", "buyer_tenant", "broker", "lender", "general_inquiry"],
                    required=True
                ),
                VariableExtraction(
                    name="initial_inquiry",
                    type="string",
                    description="Brief description of what the caller is looking for",
                    required=False
                )
            ],
            metadata={"position": {"x": -400, "y": -500}}
        )
    
    def create_caller_info_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create caller information collection node."""
        first_message = "[friendly] Great! Let me get some basic contact information from you."
        
        prompt = """You are collecting basic caller information for a commercial real estate inquiry. 
        
Ask for:
1. Full name (if not already provided)
2. Phone number for follow-up
3. Email address
4. Company name (if applicable)

Be professional and explain that this information helps us provide better service and follow-up appropriately.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "caller_name":
                variable_extractions.append(
                    VariableExtraction(
                        name="caller_name",
                        type="string",
                        description="Caller's full name",
                        required=False
                    )
                )
            elif field == "contact_phone":
                variable_extractions.append(
                    VariableExtraction(
                        name="contact_phone",
                        type="string",
                        description="Caller's phone number",
                        required=False
                    )
                )
            elif field == "contact_email":
                variable_extractions.append(
                    VariableExtraction(
                        name="contact_email",
                        type="string",
                        description="Caller's email address",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="caller_info_collection",
            name="Caller Information Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": -400, "y": -200}}
        )
    
    def create_property_info_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create property information collection node."""
        first_message = "[thoughtful] Now, let me learn more about the property you're interested in."
        
        prompt = """You are collecting property information for a commercial real estate inquiry.

Ask about:
1. Property type (office, retail, industrial, multifamily, land, mixed-use)
2. Location/market area
3. Size requirements or current size
4. Specific address (if they own the property)

Adapt your questions based on whether they're a property owner or looking to buy/lease.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "property_type":
                variable_extractions.append(
                    VariableExtraction(
                        name="property_type",
                        type="string",
                        description="Type of commercial property",
                        enum=["office", "retail", "industrial", "multifamily", "land", "mixed_use", "other"],
                        required=False
                    )
                )
            elif field == "property_location":
                variable_extractions.append(
                    VariableExtraction(
                        name="property_location",
                        type="string",
                        description="Property location or market area",
                        required=False
                    )
                )
            elif field == "property_size":
                variable_extractions.append(
                    VariableExtraction(
                        name="property_size",
                        type="string",
                        description="Property size (square feet, acres, etc.)",
                        required=False
                    )
                )
            elif field == "property_address":
                variable_extractions.append(
                    VariableExtraction(
                        name="property_address",
                        type="string",
                        description="Specific property address",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="property_info_collection",
            name="Property Information Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": -400, "y": 100}}
        )
    
    def create_transaction_info_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create transaction information collection node."""
        first_message = "[professional] Let me understand more about the transaction you're considering."
        
        prompt = """You are collecting transaction information for a commercial real estate inquiry.

Ask about:
1. Transaction type (sale, purchase, lease, tenant representation)
2. Budget range or asking price
3. Timeline for the transaction
4. Any specific requirements or constraints

Be sensitive to budget discussions and allow ranges rather than exact figures.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "transaction_type":
                variable_extractions.append(
                    VariableExtraction(
                        name="transaction_type",
                        type="string",
                        description="Type of real estate transaction",
                        enum=["sale", "purchase", "lease", "tenant_rep", "general_inquiry"],
                        required=False
                    )
                )
            elif field == "budget_range":
                variable_extractions.append(
                    VariableExtraction(
                        name="budget_range",
                        type="string",
                        description="Budget range or asking price",
                        required=False
                    )
                )
            elif field == "timeline":
                variable_extractions.append(
                    VariableExtraction(
                        name="timeline",
                        type="string",
                        description="Timeline for the transaction",
                        enum=["immediate", "1_to_3_months", "3_to_6_months", "6_plus_months", "unknown"],
                        required=False
                    )
                )
        
        return ConversationNode(
            id="transaction_info_collection",
            name="Transaction Information Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": -400, "y": 400}}
        )
    
    def create_owner_specific_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create property owner specific information collection node."""
        first_message = "[professional] Since you own the property, let me get some additional details."
        
        prompt = """You are collecting property owner specific information.

Ask about:
1. Current asking price or price expectations
2. Current rental income (if applicable)
3. Property occupancy status (occupied, vacant, partially occupied)
4. Reason for selling or leasing
5. Any specific terms or requirements

Be professional and understanding about their motivations.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "asking_price":
                variable_extractions.append(
                    VariableExtraction(
                        name="asking_price",
                        type="string",
                        description="Asking price or price expectations",
                        required=False
                    )
                )
            elif field == "current_income":
                variable_extractions.append(
                    VariableExtraction(
                        name="current_income",
                        type="string",
                        description="Current rental income from the property",
                        required=False
                    )
                )
            elif field == "property_status":
                variable_extractions.append(
                    VariableExtraction(
                        name="property_status",
                        type="string",
                        description="Current occupancy status of the property",
                        enum=["occupied", "vacant", "partially_occupied"],
                        required=False
                    )
                )
            elif field == "reason_for_selling":
                variable_extractions.append(
                    VariableExtraction(
                        name="reason_for_selling",
                        type="string",
                        description="Reason for selling or leasing the property",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="owner_specific_collection",
            name="Property Owner Specific Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": -100, "y": 700}}
        )
    
    def create_buyer_tenant_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create buyer/tenant specific information collection node."""
        first_message = "[thoughtful] Let me understand your specific requirements and preferences."
        
        prompt = """You are collecting buyer/tenant specific information.

Ask about:
1. Preferred locations or markets
2. Must-have amenities or features
3. Current location (if relocating)
4. Reason for the move or expansion
5. Any deal-breakers or constraints

Be helpful in understanding their business needs.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "preferred_locations":
                variable_extractions.append(
                    VariableExtraction(
                        name="preferred_locations",
                        type="array",
                        description="List of preferred locations or markets",
                        required=False
                    )
                )
            elif field == "must_have_amenities":
                variable_extractions.append(
                    VariableExtraction(
                        name="must_have_amenities",
                        type="array",
                        description="List of must-have amenities or features",
                        required=False
                    )
                )
            elif field == "current_location":
                variable_extractions.append(
                    VariableExtraction(
                        name="current_location",
                        type="string",
                        description="Current business location",
                        required=False
                    )
                )
            elif field == "move_reason":
                variable_extractions.append(
                    VariableExtraction(
                        name="move_reason",
                        type="string",
                        description="Reason for moving or expanding",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="buyer_tenant_collection",
            name="Buyer/Tenant Specific Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": 200, "y": 700}}
        )
    
    def create_broker_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create broker specific information collection node."""
        first_message = "[friendly] Great to connect with a fellow professional! [professional] Let me get some details about your inquiry."
        
        prompt = """You are collecting broker specific information.

Ask about:
1. Brokerage name and affiliation
2. License number (if comfortable sharing)
3. Type of collaboration (referral, co-listing, etc.)
4. Specific deal details or client needs
5. Commission structure preferences

Be professional and collegial in your approach.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "brokerage_name":
                variable_extractions.append(
                    VariableExtraction(
                        name="brokerage_name",
                        type="string",
                        description="Name of the brokerage firm",
                        required=False
                    )
                )
            elif field == "license_number":
                variable_extractions.append(
                    VariableExtraction(
                        name="license_number",
                        type="string",
                        description="Real estate license number",
                        required=False
                    )
                )
            elif field == "collaboration_type":
                variable_extractions.append(
                    VariableExtraction(
                        name="collaboration_type",
                        type="string",
                        description="Type of collaboration sought",
                        enum=["referral", "co_listing", "buyer_rep", "tenant_rep", "consultation"],
                        required=False
                    )
                )
            elif field == "deal_details":
                variable_extractions.append(
                    VariableExtraction(
                        name="deal_details",
                        type="string",
                        description="Specific deal details or client requirements",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="broker_collection",
            name="Broker Specific Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": 500, "y": 700}}
        )
    
    def create_lender_collection_node(self, missing_fields: List[str]) -> ConversationNode:
        """Create lender specific information collection node."""
        first_message = "[friendly] Thank you for reaching out! [professional] Let me understand your lending capabilities."
        
        prompt = """You are collecting lender specific information.

Ask about:
1. Types of loans offered (conventional, SBA, bridge, etc.)
2. Geographic lending area
3. Maximum loan amounts
4. Specialty areas or property types
5. Current rates and terms (if appropriate)

Be professional and focus on partnership opportunities.

Only ask for information that hasn't been provided yet."""
        
        variable_extractions = []
        for field in missing_fields:
            if field == "loan_types":
                variable_extractions.append(
                    VariableExtraction(
                        name="loan_types",
                        type="array",
                        description="Types of commercial loans offered",
                        required=False
                    )
                )
            elif field == "lending_area":
                variable_extractions.append(
                    VariableExtraction(
                        name="lending_area",
                        type="string",
                        description="Geographic area where loans are offered",
                        required=False
                    )
                )
            elif field == "max_loan_amount":
                variable_extractions.append(
                    VariableExtraction(
                        name="max_loan_amount",
                        type="string",
                        description="Maximum loan amount available",
                        required=False
                    )
                )
        
        return ConversationNode(
            id="lender_collection",
            name="Lender Specific Collection",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=variable_extractions,
            metadata={"position": {"x": 800, "y": 700}}
        )
    
    def create_lead_qualification_node(self) -> ConversationNode:
        """Create lead qualification and closing node."""
        first_message = "[professional] Perfect! Let me just confirm a few final details and next steps."
        
        prompt = """You are qualifying the lead and setting up next steps.

Assess:
1. Lead quality (hot, warm, cold) based on timeline and commitment level
2. Immediate next steps needed
3. Follow-up preferences
4. Any additional notes or requirements

Provide a professional closing that sets expectations for follow-up.

Extract the lead quality assessment and any final notes."""
        
        return ConversationNode(
            id="lead_qualification",
            name="Lead Qualification and Next Steps",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=[
                VariableExtraction(
                    name="lead_quality",
                    type="string",
                    description="Assessment of lead quality",
                    enum=["hot", "warm", "cold"],
                    required=False
                ),
                VariableExtraction(
                    name="next_steps",
                    type="string",
                    description="Agreed upon next steps",
                    required=False
                ),
                VariableExtraction(
                    name="additional_notes",
                    type="string",
                    description="Any additional notes or requirements",
                    required=False
                )
            ],
            metadata={"position": {"x": -250, "y": 1000}}
        )
    
    def create_completion_node(self) -> ToolNode:
        """Create call completion node with Google Sheets logging."""
        return ToolNode(
            id="call_completion",
            name="Call Completion and Data Logging",
            tool_type="googleSheets",
            function_name="log_cre_call_data",
            parameters={
                "spreadsheet_id": "google_sheets_spreadsheet_id",
                "sheet_name": "owner"  # Will be dynamically set based on caller type
            },
            messages=[
                {
                    "type": "request-start",
                    "content": "[friendly] Thank you so much for your time today! [professional] I have all the information I need. [reassuring] You can expect a follow-up from our team within twenty-four hours with relevant opportunities and next steps. [friendly] Have a great day!",
                    "blocking": True
                }
            ],
            metadata={"position": {"x": -250, "y": 1300}}
        )
    
    def create_general_inquiry_node(self) -> ConversationNode:
        """Create general inquiry handling node."""
        first_message = "[friendly] I'd be happy to help with your inquiry about our services."
        
        prompt = """You are handling a general inquiry about Summit Commercial Realty services.

Provide information about:
1. Our brokerage services (sales, leasing, tenant representation)
2. Market expertise and coverage areas
3. How we can help with their specific needs
4. Contact information for follow-up

Be helpful and informative while gathering any relevant details about their potential needs.

Collect any contact information and notes about their inquiry."""
        
        return ConversationNode(
            id="general_inquiry_handling",
            name="General Inquiry Handling",
            prompt=prompt,
            first_message=first_message,
            model_settings=self._get_default_model_settings(),
            transcriber_settings=self._get_default_transcriber_settings(),
            variable_extractions=[
                VariableExtraction(
                    name="inquiry_type",
                    type="string",
                    description="Type of general inquiry",
                    required=False
                ),
                VariableExtraction(
                    name="additional_notes",
                    type="string",
                    description="Notes about the inquiry and potential needs",
                    required=False
                )
            ],
            metadata={"position": {"x": 1100, "y": 700}}
        )
    
    def _get_introduction_prompt(self) -> str:
        """Get introduction node prompt."""
        return """You are Michael, a professional AI assistant for Summit Commercial Realty, a mid-tier commercial real estate brokerage. Your role is to:

1. Warmly greet callers and introduce yourself and the company
2. Identify what type of caller they are (property owner, buyer, tenant, broker, lender, or general inquiry)
3. Understand their initial needs or inquiry
4. Set a professional and helpful tone for the conversation

## Using Cartesia Sonic 3 Emotional Expressions
You can use the following inline expressions to make your voice more natural and engaging:

**Available Sonic 3 Emotions:**
- `[friendly]` - Use to convey warmth and approachability
- `[professional]` - Use for serious business matters
- `[empathetic]` - Use when understanding challenges or concerns
- `[enthusiastic]` - Use when discussing exciting opportunities
- `[thoughtful]` - Use when considering options or providing advice
- `[reassuring]` - Use when addressing concerns or objections
- `[breath]` - Use for natural pauses between sentences

**Example Usage:**
"[friendly] Hello, thank you for calling Summit Commercial Realty. This is Michael. [thoughtful] How can I help you with your commercial real estate needs today?"

Be friendly, professional, and efficient. Ask one question at a time and listen carefully to understand their needs. Use Sonic 3 expressions naturally to enhance the conversation."""
    
    def _get_introduction_first_message(self) -> str:
        """Get introduction node first message."""
        return "[friendly] Hello, thank you for calling Summit Commercial Realty. This is Michael. [thoughtful] How can I help you with your commercial real estate needs today?"
    
    def _get_default_model_settings(self) -> Dict[str, Any]:
        """Get default model settings."""
        return {
            "model": config.model_settings.model,
            "provider": config.model_settings.provider,
            "maxTokens": config.model_settings.max_tokens,
            "temperature": config.model_settings.temperature
        }
    
    def _get_default_transcriber_settings(self) -> Dict[str, Any]:
        """Get default transcriber settings."""
        return {
            "model": config.transcriber_settings.model,
            "provider": config.transcriber_settings.provider,
            "language": config.transcriber_settings.language,
            "numerals": config.transcriber_settings.numerals
        }