"""
Main orchestrator for building dynamic CRE VAPI workflows.
"""

from typing import Dict, List, Optional, Any, Union
import logging
from .models import MissingDataReport, WorkflowConfig, WorkflowEdge, ConversationNode, ToolNode, CallerCategory
from .node_factory import CRENodeFactory
from .edge_generator import CREEdgeGenerator
from .config import InformationCategory, config
from .vapi_client import VapiClient

logger = logging.getLogger(__name__)


class CREWorkflowBuilder:
    """Main orchestrator for creating dynamic CRE VAPI workflows."""
    
    def __init__(self, vapi_client: VapiClient):
        self.vapi_client = vapi_client
        self.node_factory = CRENodeFactory()
        self.edge_generator = CREEdgeGenerator()
    
    async def create_dynamic_workflow(
        self, 
        caller_type: Optional[CallerCategory] = None,
        missing_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete dynamic workflow for CRE calls.
        
        Args:
            caller_type: Optional identified caller type
            missing_fields: Optional list of missing fields to collect
            
        Returns:
            Complete workflow configuration for VAPI
        """
        logger.info(f"Creating dynamic CRE workflow for caller type: {caller_type}")
        
        try:
            # Initialize workflow configuration
            workflow_config = WorkflowConfig(
                name="cre_dynamic_workflow",
                voice_settings=self._get_voice_settings(),
                global_prompt=self._get_global_prompt()
            )
            
            # Create nodes based on caller type and missing data
            nodes = await self._create_workflow_nodes(caller_type, missing_fields)
            
            # Add nodes to workflow
            for node in nodes:
                workflow_config.add_node(node)
            
            # Create edges based on caller type and node structure
            edges = self._create_workflow_edges(caller_type, nodes)
            
            # Add edges to workflow
            for edge in edges:
                workflow_config.add_edge(edge)
            
            # Convert to VAPI format
            vapi_config = self._convert_to_vapi_format(workflow_config)
            
            logger.info(f"Successfully created workflow with {len(nodes)} nodes and {len(edges)} edges")
            return vapi_config
            
        except Exception as e:
            logger.error(f"Error creating dynamic workflow: {str(e)}")
            raise
    
    async def _create_workflow_nodes(
        self, 
        caller_type: Optional[CallerCategory] = None,
        missing_fields: Optional[List[str]] = None
    ) -> List[Union[ConversationNode, ToolNode]]:
        """Create all nodes needed for the CRE workflow."""
        nodes = []
        
        # Always add introduction node
        intro_node = self.node_factory.create_introduction_node()
        nodes.append(intro_node)
        
        # Add collection nodes based on caller type and missing fields
        if not caller_type or missing_fields:
            # Add general collection nodes
            nodes.extend(self._create_general_collection_nodes(missing_fields or []))
        
        # Add caller-specific nodes
        if caller_type:
            caller_specific_node = self._create_caller_specific_node(caller_type, missing_fields or [])
            if caller_specific_node:
                nodes.append(caller_specific_node)
        else:
            # Add all caller-specific nodes for dynamic routing
            nodes.extend(self._create_all_caller_specific_nodes(missing_fields or []))
        
        # Add lead qualification node
        lead_qual_node = self.node_factory.create_lead_qualification_node()
        nodes.append(lead_qual_node)
        
        # Add completion node
        completion_node = self.node_factory.create_completion_node()
        nodes.append(completion_node)
        
        return nodes
    
    def _create_general_collection_nodes(self, missing_fields: List[str]) -> List[ConversationNode]:
        """Create general information collection nodes."""
        nodes = []
        
        # Caller info collection
        caller_info_fields = [f for f in missing_fields if f in ["caller_name", "contact_phone", "contact_email"]]
        if caller_info_fields or not missing_fields:  # Include if no specific missing fields provided
            caller_info_node = self.node_factory.create_caller_info_collection_node(caller_info_fields)
            nodes.append(caller_info_node)
        
        # Property info collection
        property_info_fields = [f for f in missing_fields if f in ["property_type", "property_location", "property_size", "property_address"]]
        if property_info_fields or not missing_fields:
            property_info_node = self.node_factory.create_property_info_collection_node(property_info_fields)
            nodes.append(property_info_node)
        
        # Transaction info collection
        transaction_info_fields = [f for f in missing_fields if f in ["transaction_type", "budget_range", "timeline"]]
        if transaction_info_fields or not missing_fields:
            transaction_info_node = self.node_factory.create_transaction_info_collection_node(transaction_info_fields)
            nodes.append(transaction_info_node)
        
        return nodes
    
    def _create_caller_specific_node(
        self, 
        caller_type: CallerCategory, 
        missing_fields: List[str]
    ) -> Optional[Union[ConversationNode, ToolNode]]:
        """Create a caller-specific collection node."""
        
        if caller_type == CallerCategory.PROPERTY_OWNER:
            owner_fields = [f for f in missing_fields if f in ["asking_price", "current_income", "property_status", "reason_for_selling"]]
            if owner_fields or not missing_fields:
                return self.node_factory.create_owner_specific_collection_node(owner_fields)
        
        elif caller_type == CallerCategory.BUYER_TENANT:
            buyer_fields = [f for f in missing_fields if f in ["preferred_locations", "must_have_amenities", "current_location", "move_reason"]]
            if buyer_fields or not missing_fields:
                return self.node_factory.create_buyer_tenant_collection_node(buyer_fields)
        
        elif caller_type == CallerCategory.BROKER:
            broker_fields = [f for f in missing_fields if f in ["brokerage_name", "license_number", "collaboration_type", "deal_details"]]
            if broker_fields or not missing_fields:
                return self.node_factory.create_broker_collection_node(broker_fields)
        
        elif caller_type == CallerCategory.LENDER:
            lender_fields = [f for f in missing_fields if f in ["loan_types", "lending_area", "max_loan_amount"]]
            if lender_fields or not missing_fields:
                return self.node_factory.create_lender_collection_node(lender_fields)
        
        elif caller_type == CallerCategory.GENERAL_INQUIRY:
            return self.node_factory.create_general_inquiry_node()
        
        return None
    
    def _create_all_caller_specific_nodes(self, missing_fields: List[str]) -> List[ConversationNode]:
        """Create all caller-specific nodes for dynamic routing."""
        nodes = []
        
        # Create nodes for each caller type
        for caller_type in CallerCategory:
            node = self._create_caller_specific_node(caller_type, missing_fields)
            if node:
                nodes.append(node)
        
        return nodes
    
    def _create_workflow_edges(
        self, 
        caller_type: Optional[CallerCategory],
        nodes: List[Union[ConversationNode, ToolNode]]
    ) -> List[WorkflowEdge]:
        """Create edges connecting the workflow nodes."""
        logger.info("Creating workflow edges for CRE workflow")
        
        # Get node IDs for easier reference
        node_ids = [node.id for node in nodes]
        
        # Create missing data report (simplified for CRE workflow)
        missing_report = MissingDataReport()
        
        # Use EdgeGenerator to create conditional routing
        edges = self.edge_generator.create_dynamic_edges(missing_report, node_ids, caller_type)
        
        return edges
    
    def _convert_to_vapi_format(self, workflow_config: WorkflowConfig) -> Dict[str, Any]:
        """Convert internal workflow config to VAPI format."""
        logger.info("Converting workflow config to VAPI format")
        
        vapi_nodes = []
        vapi_edges = []
        
        # Convert nodes
        for node in workflow_config.nodes:
            if isinstance(node, ConversationNode):
                vapi_node = self._convert_conversation_node_to_vapi(node)
            elif isinstance(node, ToolNode):
                vapi_node = self._convert_tool_node_to_vapi(node)
            else:
                continue
            
            vapi_nodes.append(vapi_node)
        
        # Convert edges
        for edge in workflow_config.edges:
            vapi_edge = {
                "from": edge.from_node,
                "to": edge.to_node,
                "condition": {
                    "type": edge.condition_type,
                    "prompt": edge.condition_prompt
                }
            }
            vapi_edges.append(vapi_edge)
        
        return {
            "name": workflow_config.name,
            "nodes": vapi_nodes,
            "edges": vapi_edges,
            "voice": workflow_config.voice_settings,
            "globalPrompt": workflow_config.global_prompt
        }
    
    def _convert_conversation_node_to_vapi(self, node: ConversationNode) -> Dict[str, Any]:
        """Convert ConversationNode to VAPI format."""
        vapi_node = {
            "name": node.id,
            "type": "conversation",
            "metadata": node.metadata or {}
        }
        
        # Add isStart flag for introduction node
        if node.id == "introduction":
            vapi_node["isStart"] = True
        
        # Add prompt
        if node.prompt:
            vapi_node["prompt"] = node.prompt
        
        # Add model settings
        if node.model_settings:
            vapi_node["model"] = node.model_settings
        
        # Add transcriber settings
        if node.transcriber_settings:
            vapi_node["transcriber"] = node.transcriber_settings
        
        # Add variable extraction plan
        if node.variable_extractions:
            schema_properties = {}
            for var in node.variable_extractions:
                prop = {
                    "type": var.type,
                    "description": var.description
                }
                if var.enum:
                    prop["enum"] = var.enum
                schema_properties[var.name] = prop
            
            vapi_node["variableExtractionPlan"] = {
                "schema": {
                    "type": "object",
                    "properties": schema_properties
                }
            }
        
        # Add message plan
        if node.first_message:
            vapi_node["messagePlan"] = {
                "firstMessage": node.first_message
            }
        
        # Add global flag if applicable
        if node.is_global:
            vapi_node["isGlobal"] = True
        
        # Add condition if applicable
        if node.condition:
            vapi_node["condition"] = node.condition
        
        return vapi_node
    
    def _convert_tool_node_to_vapi(self, node: ToolNode) -> Dict[str, Any]:
        """Convert ToolNode to VAPI format."""
        vapi_node = {
            "name": node.id,
            "type": "tool",
            "metadata": node.metadata or {}
        }
        
        # Handle different tool types
        if node.tool_type == "googleSheets":
            vapi_node["tool"] = {
                "type": "function",
                "function": {
                    "name": node.function_name,
                    "parameters": {
                        "type": "object",
                        "required": [],
                        "properties": node.parameters
                    }
                }
            }
        elif node.tool_type == "endCall":
            vapi_node["tool"] = {
                "type": "endCall"
            }
        
        # Add messages if provided
        if node.messages:
            vapi_node["tool"]["messages"] = node.messages
        
        return vapi_node
    
    def _get_voice_settings(self) -> Dict[str, Any]:
        """Get voice settings for the workflow."""
        return {
            "provider": "cartesia",
            "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",  # Cartesia Sonic 3 voice
            "model": "sonic-3",
            "speed": 1.0,
            "stability": 0.5,
            "similarityBoost": 0.75,
            "style": 0.0,
            "useSpeakerBoost": True
        }
    
    def _get_global_prompt(self) -> str:
        """Get global prompt for the CRE workflow."""
        return """## System Identity
You are Michael, a professional AI assistant for Summit Commercial Realty, a mid-tier commercial real estate brokerage. You specialize in helping clients with office, retail, industrial, multifamily, and land transactions.

## Your Mission
You are handling inbound calls to qualify leads and gather information about potential commercial real estate transactions. Your goal is to collect comprehensive information to help our brokers provide the best possible service.

## Communication Guidelines
- **Tone**: Professional, knowledgeable, and helpful with natural expressiveness
- **Language**: Use commercial real estate terminology appropriately
- **Approach**: One question at a time, listen actively, be thorough but efficient
- **Voice**: Use Cartesia Sonic 3 emotional expressions naturally for warmth and professionalism

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

**Usage Guidelines:**
- Use expressions naturally and sparingly (1-2 per conversation segment)
- Match expressions to the conversation context
- Always maintain professionalism even with expressions
- Use [breath] for natural pauses instead of "um" or "uh"

## Core Behaviors
1. **Be Professional**: Maintain a business-appropriate tone throughout
2. **Be Thorough**: Collect all relevant information for proper lead qualification
3. **Be Efficient**: Don't waste the caller's time with unnecessary questions
4. **Be Helpful**: Provide value and set proper expectations for follow-up

## Conversation Guidelines
- Always introduce yourself and Summit Commercial Realty
- Identify the caller type early (property owner, buyer, tenant, broker, lender, general inquiry)
- Ask one question at a time and wait for responses
- Adapt your questions based on the caller type and their specific needs
- Be sensitive when discussing financial information (budgets, prices, income)
- Confirm important details to ensure accuracy
- Set clear expectations for follow-up and next steps

## Lead Qualification
- Assess timeline urgency (immediate, 1-3 months, 3-6 months, 6+ months)
- Understand decision-making authority
- Gauge seriousness and commitment level
- Identify any immediate opportunities or urgent needs

## Data Collection Principles
- Collect contact information early for follow-up purposes
- Understand property details thoroughly (type, location, size, condition)
- Gather transaction specifics (sale vs lease, budget ranges, timeline)
- Identify specific needs, preferences, and deal-breakers
- Note any special circumstances or requirements

## Professional Standards
- Respect confidentiality and handle sensitive information appropriately
- Be honest about our capabilities and market coverage
- Provide realistic timelines and expectations
- Maintain Summit Commercial Realty's reputation for professionalism

## Remember
You're not just collecting information - you're representing Summit Commercial Realty and building relationships that could lead to successful transactions. Be genuinely helpful and make callers feel confident in our ability to serve their commercial real estate needs."""
    
    async def update_existing_workflow(
        self, 
        workflow_id: str, 
        caller_type: Optional[CallerCategory] = None,
        missing_fields: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing workflow with new requirements.
        
        Args:
            workflow_id: Existing VAPI workflow ID
            caller_type: Updated caller type
            missing_fields: Updated missing fields list
            
        Returns:
            Updated workflow configuration
        """
        logger.info(f"Updating existing workflow: {workflow_id}")
        
        try:
            # Create new workflow configuration
            new_config = await self.create_dynamic_workflow(caller_type, missing_fields)
            
            # Update the workflow in VAPI
            updated_workflow = await self.vapi_client.update_workflow(workflow_id, new_config)
            
            logger.info(f"Successfully updated workflow: {workflow_id}")
            return updated_workflow
            
        except Exception as e:
            logger.error(f"Error updating workflow: {str(e)}")
            raise