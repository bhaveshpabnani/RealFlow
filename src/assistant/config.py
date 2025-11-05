"""Configuration settings for RealFlow CRE Agent"""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Vapi Configuration
    vapi_api_key: str
    vapi_base_url: str = "https://api.vapi.ai"
    vapi_phone_number_id: Optional[str] = None
    vapi_phone_number: Optional[str] = None
    
    # Google Sheets Configuration
    google_sheets_credentials_file: str = "credentials.json"
    google_sheets_spreadsheet_id: str
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    
    # Webhook Configuration
    webhook_base_url: str
    webhook_secret: str
    
    # Assistant Configuration
    assistant_id: str
    phone_number: str
    
    # Brokerage Information
    brokerage_name: str = "Summit Commercial Realty"
    brokerage_website: str = "https://summitcommercialrealty.com"
    agent_name: str = "Michael"
    
    # Cartesia Sonic 3 Voice Configuration
    cartesia_voice_id: Optional[str] = "57dcab65-68ac-45a6-8480-6c4c52ec1cd1"
    cartesia_model_id: Optional[str] = "sonic-3"
    cartesia_provider: Optional[str] = "cartesia"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()