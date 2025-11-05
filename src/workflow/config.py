"""
Configuration management for RealFlow CRE workflow implementation.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum
from .models import CallerCategory

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv is not available, try to load manually
    import pathlib
    env_path = pathlib.Path(__file__).parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value


class InformationCategory(Enum):
    """Categories of information to collect from CRE callers."""
    CALLER_INFO = "caller_info"
    PROPERTY_INFO = "property_info"
    TRANSACTION_INFO = "transaction_info"
    SPECIFIC_DETAILS = "specific_details"


@dataclass
class VoiceSettings:
    """Voice configuration for CRE agent."""
    voice_id: str
    model: str
    provider: str = "cartesia"
    speed: float = 1.0
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True


@dataclass
class ModelSettings:
    """AI model configuration."""
    model: str = "gpt-4o"
    provider: str = "openai"
    max_tokens: int = 500
    temperature: float = 0.3


@dataclass
class TranscriberSettings:
    """Speech transcription configuration."""
    model: str = "nova-2"
    provider: str = "deepgram"
    language: str = "en-US"
    numerals: bool = True


@dataclass
class ApiSettings:
    """API configuration settings."""
    vapi_api_key: str
    vapi_base_url: str = "https://api.vapi.ai"
    vapi_phone_number_id: Optional[str] = None
    vapi_phone_number: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3


@dataclass
class RetrySettings:
    """Retry configuration for API calls."""
    max_attempts: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0


@dataclass
class FieldMappingConfig:
    """Centralized field mapping configuration for CRE data."""
    
    # Google Sheets column mapping
    SHEETS_MAPPING = {
        'timestamp': 'Timestamp',
        'caller_name': 'Caller Name',
        'caller_type': 'Caller Type',
        'property_type': 'Property Type',
        'property_location': 'Market Location',
        'transaction_type': 'Transaction Type',
        'budget_range': 'Size/Budget',
        'timeline': 'Timeline',
        'contact_phone': 'Contact Phone',
        'contact_email': 'Contact Email',
        'additional_notes': 'Additional Notes',
        'lead_quality': 'Lead Quality',
        'call_duration': 'Call Duration'
    }
    
    # Owner-specific fields
    OWNER_MAPPING = {
        'property_address': 'Property Address',
        'property_size': 'Property Size',
        'asking_price': 'Asking Price',
        'current_income': 'Current Income',
        'property_status': 'Property Status',
        'reason_for_selling': 'Reason for Selling'
    }
    
    # Buyer/Tenant-specific fields
    BUYER_TENANT_MAPPING = {
        'preferred_locations': 'Preferred Locations',
        'must_have_amenities': 'Must-Have Amenities',
        'current_location': 'Current Location',
        'move_reason': 'Move Reason'
    }
    
    # Broker-specific fields
    BROKER_MAPPING = {
        'brokerage_name': 'Brokerage Name',
        'license_number': 'License Number',
        'collaboration_type': 'Collaboration Type',
        'deal_details': 'Deal Details'
    }
    
    # Lender-specific fields
    LENDER_MAPPING = {
        'loan_types': 'Loan Types',
        'lending_area': 'Lending Area',
        'max_loan_amount': 'Max Loan Amount'
    }


class ConfigManager:
    """Manages configuration for RealFlow CRE workflow."""
    
    # Priority order for information collection
    COLLECTION_PRIORITY = [
        InformationCategory.CALLER_INFO,
        InformationCategory.PROPERTY_INFO,
        InformationCategory.TRANSACTION_INFO,
        InformationCategory.SPECIFIC_DETAILS,
    ]
    
    # Field priority within each category
    FIELD_PRIORITIES = {
        InformationCategory.CALLER_INFO: [
            "caller_name",
            "caller_type",
            "contact_phone",
            "contact_email"
        ],
        InformationCategory.PROPERTY_INFO: [
            "property_type",
            "property_location",
            "property_size",
            "property_address"
        ],
        InformationCategory.TRANSACTION_INFO: [
            "transaction_type",
            "budget_range",
            "timeline"
        ],
        InformationCategory.SPECIFIC_DETAILS: [
            "asking_price",
            "current_income",
            "preferred_locations",
            "brokerage_name",
            "loan_types"
        ]
    }
    
    # Caller type specific field requirements
    CALLER_TYPE_FIELDS = {
        CallerCategory.PROPERTY_OWNER: [
            "property_address", "property_size", "asking_price", 
            "current_income", "property_status", "reason_for_selling"
        ],
        CallerCategory.BUYER_TENANT: [
            "preferred_locations", "must_have_amenities", 
            "current_location", "move_reason"
        ],
        CallerCategory.BROKER: [
            "brokerage_name", "license_number", 
            "collaboration_type", "deal_details"
        ],
        CallerCategory.LENDER: [
            "loan_types", "lending_area", "max_loan_amount"
        ],
        CallerCategory.GENERAL_INQUIRY: [
            "additional_notes"
        ]
    }
    
    def __init__(self):
        try:
            self.api_settings = self._load_api_settings()
            self.voice_settings = self._load_voice_settings()
            self.model_settings = ModelSettings()
            self.transcriber_settings = TranscriberSettings()
            self.retry_settings = RetrySettings()
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Configuration loading warning: {str(e)}. Some features may not work until environment variables are properly set.")
            # Set default values to allow import to succeed
            self.api_settings = ApiSettings(vapi_api_key="placeholder")
            self.voice_settings = VoiceSettings(voice_id="placeholder", model="placeholder")
            self.model_settings = ModelSettings()
            self.transcriber_settings = TranscriberSettings()
            self.retry_settings = RetrySettings()
    
    def _load_api_settings(self) -> ApiSettings:
        """Load API settings from environment variables."""
        api_key = os.getenv("VAPI_API_KEY")
        if not api_key:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("VAPI_API_KEY not found in environment variables.")
            logger.warning("Available environment variables starting with VAPI:")
            for key in os.environ:
                if key.startswith("VAPI"):
                    logger.warning(f"  {key}={os.environ[key][:10]}...")
            raise ValueError("VAPI_API_KEY environment variable is required")
        
        return ApiSettings(
            vapi_api_key=api_key,
            vapi_base_url=os.getenv("VAPI_BASE_URL", "https://api.vapi.ai"),
            vapi_phone_number_id=os.getenv("VAPI_PHONE_NUMBER_ID"),
            vapi_phone_number=os.getenv("VAPI_PHONE_NUMBER"),
            timeout=int(os.getenv("VAPI_TIMEOUT", "30")),
            max_retries=int(os.getenv("VAPI_MAX_RETRIES", "3"))
        )
    
    def _load_voice_settings(self) -> VoiceSettings:
        """Load voice settings from environment variables."""
        # Use Cartesia Sonic 3 voice settings (preferred) or fallback to ElevenLabs
        voice_id = os.getenv("CARTESIA_VOICE_ID", "57dcab65-68ac-45a6-8480-6c4c52ec1cd1")
        model_id = os.getenv("CARTESIA_MODEL_ID", "sonic-3")
        provider = os.getenv("CARTESIA_PROVIDER", "cartesia")
        
        # Fallback to ElevenLabs if Cartesia not configured
        if not os.getenv("CARTESIA_VOICE_ID") and os.getenv("ELEVENLABS_VOICE_ID"):
            voice_id = os.getenv("ELEVENLABS_VOICE_ID")
            model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5")
            provider = "11labs"
        
        return VoiceSettings(
            voice_id=voice_id,
            model=model_id,
            provider=provider,
            speed=1.0,
            stability=0.5,
            similarity_boost=0.75,
            style=0.0,
            use_speaker_boost=True
        )
    
    def get_field_priority_order(self, category: InformationCategory) -> List[str]:
        """Get priority order for fields within a category."""
        return self.FIELD_PRIORITIES.get(category, [])
    
    def get_collection_priority_order(self) -> List[InformationCategory]:
        """Get priority order for information collection categories."""
        return self.COLLECTION_PRIORITY.copy()
    
    def get_caller_type_fields(self, caller_type: CallerCategory) -> List[str]:
        """Get required fields for a specific caller type."""
        return self.CALLER_TYPE_FIELDS.get(caller_type, [])


# Global configuration instance
config = ConfigManager()