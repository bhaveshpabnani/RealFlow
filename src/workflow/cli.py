"""
Command Line Interface for RealFlow CRE Workflow System
"""

import asyncio
import click
import json
from typing import Optional
from .cre_workflow import CREWorkflow
from .models import CallerCategory
from .setup_tools import CREWorkflowSetup
from .config import config


@click.group()
def cli():
    """RealFlow CRE Workflow System CLI"""
    pass


@cli.command()
@click.option('--caller-type', type=click.Choice(['property_owner', 'buyer_tenant', 'broker', 'lender', 'general_inquiry']), help='Caller type for the workflow')
@click.option('--name', help='Workflow name')
def create_workflow(caller_type: Optional[str], name: Optional[str]):
    """Create a new workflow"""
    async def _create():
        workflow_manager = CREWorkflow()
        
        caller_enum = None
        if caller_type:
            caller_enum = CallerCategory(caller_type)
        
        result = await workflow_manager.create_dynamic_workflow(
            caller_type=caller_enum,
            workflow_name=name or f"CLI Workflow - {caller_type or 'General'}"
        )
        
        click.echo(f"✅ Created workflow: {result['workflow_id']}")
        click.echo(f"   Status: {result['status']}")
        click.echo(f"   Caller Type: {result.get('caller_type', 'Any')}")
        
        return result
    
    return asyncio.run(_create())


@cli.command()
@click.argument('phone_number')
@click.option('--caller-type', type=click.Choice(['property_owner', 'buyer_tenant', 'broker', 'lender', 'general_inquiry']), help='Caller type')
@click.option('--workflow-id', help='Existing workflow ID to use')
def initiate_call(phone_number: str, caller_type: Optional[str], workflow_id: Optional[str]):
    """Initiate a call to the specified phone number"""
    async def _initiate():
        workflow_manager = CREWorkflow()
        
        caller_enum = None
        if caller_type:
            caller_enum = CallerCategory(caller_type)
        
        result = await workflow_manager.initiate_call(
            customer_phone=phone_number,
            caller_type=caller_enum,
            workflow_id=workflow_id
        )
        
        click.echo(f"✅ Call initiated: {result['call_id']}")
        click.echo(f"   Phone: {result['customer_phone']}")
        click.echo(f"   Workflow: {result['workflow_id']}")
        click.echo(f"   Status: {result['status']}")
        
        return result
    
    return asyncio.run(_initiate())


@cli.command()
@click.argument('call_id')
def call_status(call_id: str):
    """Get call status"""
    async def _status():
        workflow_manager = CREWorkflow()
        result = await workflow_manager.get_call_status(call_id)
        
        if result:
            click.echo(f"📞 Call Status: {result['status']}")
            click.echo(f"   Duration: {result.get('duration', 'N/A')} seconds")
            click.echo(f"   Data Collected: {len(result.get('collected_data', {}))} fields")
            
            if result.get('collected_data'):
                click.echo("\n📊 Collected Data:")
                for key, value in result['collected_data'].items():
                    click.echo(f"   {key}: {value}")
        else:
            click.echo(f"❌ Call not found: {call_id}")
        
        return result
    
    return asyncio.run(_status())


@cli.command()
def list_workflows():
    """List all workflows"""
    async def _list():
        workflow_manager = CREWorkflow()
        workflows = await workflow_manager.list_workflows()
        
        click.echo(f"📋 Found {len(workflows)} workflows:")
        for workflow in workflows:
            click.echo(f"   {workflow.get('id', 'N/A')}: {workflow.get('name', 'Unnamed')}")
        
        return workflows
    
    return asyncio.run(_list())


@cli.command()
@click.option('--limit', default=10, help='Number of recent calls to show')
def list_calls(limit: int):
    """List recent calls"""
    async def _list():
        workflow_manager = CREWorkflow()
        calls = await workflow_manager.list_calls(limit)
        
        click.echo(f"📞 Found {len(calls)} recent calls:")
        for call in calls:
            status = call.get('status', 'unknown')
            duration = call.get('duration', 'N/A')
            click.echo(f"   {call.get('id', 'N/A')}: {status} ({duration}s)")
        
        return calls
    
    return asyncio.run(_list())


@cli.command()
@click.argument('spreadsheet_id')
@click.argument('phone_number')
@click.option('--credentials', default='credentials.json', help='Path to Google credentials file')
def setup_system(spreadsheet_id: str, phone_number: str, credentials: str):
    """Setup complete workflow system"""
    async def _setup():
        setup_manager = CREWorkflowSetup()
        
        click.echo("🛠️  Setting up complete CRE workflow system...")
        
        result = await setup_manager.setup_complete_system(
            spreadsheet_id=spreadsheet_id,
            phone_number=phone_number,
            credentials_path=credentials
        )
        
        click.echo("✅ Setup completed!")
        click.echo(f"   Workflow ID: {result['workflow_id']}")
        click.echo(f"   Phone Number ID: {result['phone_number_id']}")
        click.echo(f"   Tools Created: {len(result['tool_ids'])}")
        
        return result
    
    return asyncio.run(_setup())


@cli.command()
def test_connection():
    """Test VAPI and Google Sheets connections"""
    async def _test():
        from .vapi_client import VapiClient
        from .services.sheets_service import WorkflowSheetsService
        import os
        
        click.echo("🔍 Testing connections...")
        
        # Test VAPI
        try:
            vapi_client = VapiClient()
            workflows = await vapi_client.list_workflows()
            click.echo(f"✅ VAPI: Connected ({len(workflows)} workflows)")
        except Exception as e:
            click.echo(f"❌ VAPI: Failed - {str(e)}")
        
        # Test Google Sheets
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")
        credentials_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
        
        if spreadsheet_id and os.path.exists(credentials_path):
            try:
                sheets_service = WorkflowSheetsService(credentials_path, spreadsheet_id)
                test_result = sheets_service.test_connection()
                if test_result["status"] == "connected":
                    click.echo(f"✅ Google Sheets: Connected ({test_result['worksheet_count']} sheets)")
                else:
                    click.echo(f"❌ Google Sheets: {test_result['error']}")
            except Exception as e:
                click.echo(f"❌ Google Sheets: Failed - {str(e)}")
        else:
            click.echo("⚠️  Google Sheets: Not configured")
    
    return asyncio.run(_test())


@cli.command()
def config_info():
    """Show configuration information"""
    click.echo("⚙️  Configuration Information:")
    click.echo(f"   VAPI API Key: {'*' * (len(config.api_settings.vapi_api_key) - 4) + config.api_settings.vapi_api_key[-4:]}")
    click.echo(f"   VAPI Base URL: {config.api_settings.vapi_base_url}")
    click.echo(f"   Phone Number: {config.api_settings.vapi_phone_number or 'Not set'}")
    click.echo(f"   Voice Provider: {config.voice_settings.provider}")
    click.echo(f"   Voice ID: {config.voice_settings.voice_id}")
    click.echo(f"   Model: {config.model_settings.model}")
    click.echo(f"   Collection Categories: {len(config.get_collection_priority_order())}")


if __name__ == '__main__':
    cli()