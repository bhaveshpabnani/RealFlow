"""
Generates conditional edges for dynamic CRE VAPI workflows.
"""

from typing import Dict, List, Optional, Any
import logging
from .models import WorkflowEdge, MissingDataReport, CallerCategory
from .config import InformationCategory

logger = logging.getLogger(__name__)


class CREEdgeGenerator:
    """Generates conditional routing edges for CRE VAPI workflows."""
    
    def create_dynamic_edges(
        self, 
        missing_report: MissingDataReport, 
        node_ids: List[str],
        caller_type: Optional[CallerCategory] = None
    ) -> List[WorkflowEdge]:
        """
        Create dynamic edges based on missing data analysis and caller type.
        
        Args:
            missing_report: Analysis of missing data
            node_ids: List of available node IDs
            caller_type: Identified caller type for routing
            
        Returns:
            List of workflow edges with conditional routing
        """
        logger.info("Creating dynamic edges for CRE workflow routing")
        
        edges = []
        
        # Create edges from introduction node
        edges.extend(self._create_introduction_edges(node_ids, caller_type))
        
        # Create edges between collection nodes
        edges.extend(self._create_collection_edges(missing_report, node_ids, caller_type))
        
        # Create edges to completion nodes
        edges.extend(self._create_completion_edges(node_ids))
        
        logger.info(f"Created {len(edges)} dynamic edges")
        return edges
    
    def _create_introduction_edges(
        self, 
        node_ids: List[str],
        caller_type: Optional[CallerCategory] = None
    ) -> List[WorkflowEdge]:
        """Create edges from the introduction node based on caller type."""
        edges = []
        
        # Route to appropriate collection node based on caller type
        if "caller_info_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="caller_info_collection",
                condition_type="ai",
                condition_prompt="if caller_type is identified and we need to collect basic contact information"
            ))
        
        # Direct routing for specific caller types
        if "owner_specific_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="owner_specific_collection",
                condition_type="ai",
                condition_prompt="if caller_type is property_owner and basic info is complete"
            ))
        
        if "buyer_tenant_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="buyer_tenant_collection",
                condition_type="ai",
                condition_prompt="if caller_type is buyer_tenant and basic info is complete"
            ))
        
        if "broker_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="broker_collection",
                condition_type="ai",
                condition_prompt="if caller_type is broker and basic info is complete"
            ))
        
        if "lender_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="lender_collection",
                condition_type="ai",
                condition_prompt="if caller_type is lender and basic info is complete"
            ))
        
        if "general_inquiry_handling" in node_ids:
            edges.append(WorkflowEdge(
                from_node="introduction",
                to_node="general_inquiry_handling",
                condition_type="ai",
                condition_prompt="if caller_type is general_inquiry"
            ))
        
        return edges
    
    def _create_collection_edges(
        self, 
        missing_report: MissingDataReport, 
        node_ids: List[str],
        caller_type: Optional[CallerCategory] = None
    ) -> List[WorkflowEdge]:
        """Create edges between collection nodes."""
        edges = []
        
        # From caller_info_collection to property_info_collection
        if "caller_info_collection" in node_ids and "property_info_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="caller_info_collection",
                to_node="property_info_collection",
                condition_type="ai",
                condition_prompt="if basic caller information is collected and property information is needed"
            ))
        
        # From property_info_collection to transaction_info_collection
        if "property_info_collection" in node_ids and "transaction_info_collection" in node_ids:
            edges.append(WorkflowEdge(
                from_node="property_info_collection",
                to_node="transaction_info_collection",
                condition_type="ai",
                condition_prompt="if property information is collected and transaction details are needed"
            ))
        
        # From transaction_info_collection to caller-specific nodes
        if "transaction_info_collection" in node_ids:
            if "owner_specific_collection" in node_ids:
                edges.append(WorkflowEdge(
                    from_node="transaction_info_collection",
                    to_node="owner_specific_collection",
                    condition_type="ai",
                    condition_prompt="if caller_type is property_owner and owner-specific information is needed"
                ))
            
            if "buyer_tenant_collection" in node_ids:
                edges.append(WorkflowEdge(
                    from_node="transaction_info_collection",
                    to_node="buyer_tenant_collection",
                    condition_type="ai",
                    condition_prompt="if caller_type is buyer_tenant and buyer/tenant-specific information is needed"
                ))
            
            if "broker_collection" in node_ids:
                edges.append(WorkflowEdge(
                    from_node="transaction_info_collection",
                    to_node="broker_collection",
                    condition_type="ai",
                    condition_prompt="if caller_type is broker and broker-specific information is needed"
                ))
            
            if "lender_collection" in node_ids:
                edges.append(WorkflowEdge(
                    from_node="transaction_info_collection",
                    to_node="lender_collection",
                    condition_type="ai",
                    condition_prompt="if caller_type is lender and lender-specific information is needed"
                ))
        
        # From caller-specific nodes to lead qualification
        caller_specific_nodes = [
            "owner_specific_collection",
            "buyer_tenant_collection", 
            "broker_collection",
            "lender_collection"
        ]
        
        for node in caller_specific_nodes:
            if node in node_ids and "lead_qualification" in node_ids:
                edges.append(WorkflowEdge(
                    from_node=node,
                    to_node="lead_qualification",
                    condition_type="ai",
                    condition_prompt="if caller-specific information is collected and ready for lead qualification"
                ))
        
        # From general inquiry to lead qualification
        if "general_inquiry_handling" in node_ids and "lead_qualification" in node_ids:
            edges.append(WorkflowEdge(
                from_node="general_inquiry_handling",
                to_node="lead_qualification",
                condition_type="ai",
                condition_prompt="if general inquiry is handled and ready for next steps"
            ))
        
        # Alternative direct paths when information is already complete
        collection_nodes = [
            "caller_info_collection",
            "property_info_collection", 
            "transaction_info_collection"
        ]
        
        for node in collection_nodes:
            if node in node_ids and "lead_qualification" in node_ids:
                edges.append(WorkflowEdge(
                    from_node=node,
                    to_node="lead_qualification",
                    condition_type="ai",
                    condition_prompt="if all required information is collected and ready for lead qualification"
                ))
        
        return edges
    
    def _create_completion_edges(self, node_ids: List[str]) -> List[WorkflowEdge]:
        """Create edges to completion nodes."""
        edges = []
        
        # From lead qualification to completion
        if "lead_qualification" in node_ids and "call_completion" in node_ids:
            edges.append(WorkflowEdge(
                from_node="lead_qualification",
                to_node="call_completion",
                condition_type="ai",
                condition_prompt="if lead qualification is complete and all information is gathered"
            ))
        
        # Direct completion paths for when all info is already available
        completion_source_nodes = [
            "caller_info_collection",
            "property_info_collection",
            "transaction_info_collection",
            "owner_specific_collection",
            "buyer_tenant_collection",
            "broker_collection",
            "lender_collection",
            "general_inquiry_handling"
        ]
        
        for node in completion_source_nodes:
            if node in node_ids and "call_completion" in node_ids:
                edges.append(WorkflowEdge(
                    from_node=node,
                    to_node="call_completion",
                    condition_type="ai",
                    condition_prompt="if all required information is collected and ready to complete the call"
                ))
        
        return edges
    
    def _get_next_collection_node(
        self, 
        current_node: str, 
        missing_report: MissingDataReport,
        node_ids: List[str]
    ) -> Optional[str]:
        """Get the next collection node based on missing data priority."""
        
        # Define the collection flow order
        collection_flow = [
            "caller_info_collection",
            "property_info_collection", 
            "transaction_info_collection"
        ]
        
        try:
            current_index = collection_flow.index(current_node)
            # Return next node in flow if it exists and is in node_ids
            for i in range(current_index + 1, len(collection_flow)):
                next_node = collection_flow[i]
                if next_node in node_ids:
                    return next_node
        except ValueError:
            # Current node not in standard flow
            pass
        
        return None
    
    def _get_caller_specific_node(self, caller_type: CallerCategory, node_ids: List[str]) -> Optional[str]:
        """Get the appropriate caller-specific collection node."""
        
        caller_node_mapping = {
            CallerCategory.PROPERTY_OWNER: "owner_specific_collection",
            CallerCategory.BUYER_TENANT: "buyer_tenant_collection",
            CallerCategory.BROKER: "broker_collection",
            CallerCategory.LENDER: "lender_collection",
            CallerCategory.GENERAL_INQUIRY: "general_inquiry_handling"
        }
        
        target_node = caller_node_mapping.get(caller_type)
        return target_node if target_node in node_ids else None