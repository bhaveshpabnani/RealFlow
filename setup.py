"""Setup script for RealFlow CRE Agent"""

import asyncio
import json
import os
from src.assistant.tools.assistant_manager import AssistantManager
from src.assistant.tools.phone_manager import PhoneManager
from src.assistant.services.sheets_service import GoogleSheetsService
from src.assistant.config import settings


async def setup_tools():
    """Setup Google Sheets tools"""
    print("🔧 Setting up Google Sheets tools...")
    
    assistant_manager = AssistantManager()
    tools = await assistant_manager.create_tools()
    
    # Save tool IDs
    tool_ids = [tool.get('id') for tool in tools]
    
    with open('tool_ids.json', 'w') as f:
        json.dump({
            'tool_ids': tool_ids,
            'tools': tools
        }, f, indent=2)
    
    print(f"✅ Created {len(tools)} tools")
    print(f"💾 Tool IDs saved to tool_ids.json")
    
    return tool_ids


async def setup_assistant():
    """Setup or update assistant"""
    print("🤖 Setting up assistant...")
    
    assistant_manager = AssistantManager()
    
    try:
        # Try to get existing assistant
        assistant = await assistant_manager.get_assistant()
        print(f"✅ Found existing assistant: {assistant.get('name')}")
        
        # Update assistant with latest config
        assistant = await assistant_manager.update_assistant()
        print("✅ Updated assistant configuration")
        
    except Exception as e:
        print(f"❌ Error getting existing assistant: {e}")
        print("🔄 Creating new assistant...")
        
        # Create new assistant
        assistant = await assistant_manager.create_assistant()
        print(f"✅ Created new assistant: {assistant.get('name')}")
        
        # Save assistant ID
        assistant_id = assistant.get('id')
        with open('assistant_id.txt', 'w') as f:
            f.write(assistant_id)
        print(f"💾 Assistant ID saved: {assistant_id}")
    
    return assistant


async def setup_phone_number():
    """Setup phone number"""
    print("📞 Setting up phone number...")
    
    phone_manager = PhoneManager()
    webhook_url = f"{settings.webhook_base_url}/webhook/vapi"
    
    try:
        phone_number = await phone_manager.setup_phone_number(
            settings.assistant_id, 
            webhook_url
        )
        print(f"✅ Phone number setup complete: {phone_number.get('number')}")
        return phone_number
    except Exception as e:
        print(f"❌ Error setting up phone number: {e}")
        return None


def setup_google_sheets():
    """Setup Google Sheets"""
    print("📊 Setting up Google Sheets...")
    
    sheets_service = GoogleSheetsService()
    
    if sheets_service.client:
        print("✅ Google Sheets connection successful")
        
        # Test creating worksheets
        test_sheets = ["owner", "customer", "broker"]
        for sheet_name in test_sheets:
            worksheet = sheets_service._get_or_create_worksheet(sheet_name)
            if worksheet:
                print(f"✅ Worksheet '{sheet_name}' ready")
            else:
                print(f"❌ Failed to create worksheet '{sheet_name}'")
        
        return True
    else:
        print("❌ Google Sheets connection failed")
        print("   Please check your credentials.json file")
        return False


def check_environment():
    """Check environment setup"""
    print("🔍 Checking environment...")
    
    required_vars = [
        'VAPI_API_KEY',
        'GOOGLE_SHEETS_SPREADSHEET_ID',
        'ASSISTANT_ID',
        'PHONE_NUMBER',
        'BROKERAGE_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var.lower(), None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("   Please check your .env file")
        return False
    
    print("✅ Environment variables OK")
    
    # Check credentials file
    if not os.path.exists(settings.google_sheets_credentials_file):
        print(f"❌ Google Sheets credentials file not found: {settings.google_sheets_credentials_file}")
        print("   Please download your service account credentials from Google Cloud Console")
        return False
    
    print("✅ Google Sheets credentials file found")
    return True


async def main():
    """Main setup function"""
    print("🚀 RealFlow CRE Agent Setup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment check failed. Please fix the issues above.")
        return
    
    # Setup Google Sheets
    if not setup_google_sheets():
        print("\n❌ Google Sheets setup failed.")
        return
    
    # Setup tools
    try:
        tool_ids = await setup_tools()
    except Exception as e:
        print(f"❌ Tool setup failed: {e}")
        return
    
    # Setup assistant
    try:
        assistant = await setup_assistant()
    except Exception as e:
        print(f"❌ Assistant setup failed: {e}")
        return
    
    # Setup phone number
    try:
        phone_number = await setup_phone_number()
    except Exception as e:
        print(f"❌ Phone number setup failed: {e}")
        return
    
    print("\n" + "=" * 50)
    print("✅ RealFlow CRE Agent Setup Complete!")
    print("=" * 50)
    print(f"🏢 Brokerage: {settings.brokerage_name}")
    print(f"🤖 Assistant: {settings.agent_name}")
    print(f"📞 Phone: {settings.phone_number}")
    print(f"🆔 Assistant ID: {settings.assistant_id}")
    print(f"📊 Google Sheets: {settings.google_sheets_spreadsheet_id}")
    print(f"🌐 Webhook URL: {settings.webhook_base_url}/webhook/vapi")
    print("\n🎉 Your AI agent is ready to take calls!")


if __name__ == "__main__":
    asyncio.run(main())