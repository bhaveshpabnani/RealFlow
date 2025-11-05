"""
Predefined RealFlow CRE Workflow Template
Similar to AIRA workflow but optimized for commercial real estate
"""

from typing import Dict, Any


def get_realflow_cre_workflow_template(workflow_name: str = "RealFlow CRE Workflow") -> Dict[str, Any]:
    """
    Get the predefined RealFlow CRE workflow template with separate branching for different caller types.
    
    Args:
        workflow_name: Name for the workflow
        
    Returns:
        Complete VAPI workflow configuration with caller-specific paths
    """
    return {
        "name": workflow_name,
        "nodes": [
            {
                "name": "introduction",
                "type": "conversation",
                "isStart": True,
                "metadata": {
                    "position": {
                        "x": -400,
                        "y": -500
                    }
                },
                "prompt": "You are Michael from Summit Commercial Realty. Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.3
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "yes",
                                "no",
                                "later"
                            ],
                            "type": "string",
                            "title": "call_consent",
                            "description": "Whether the caller consents to proceed with the CRE discussion"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[friendly] Hello, thank you for calling Summit Commercial Realty. This is Michael. How may I assist you with your commercial real estate needs today?"
                },
                "toolIds": []
            },
            {
                "name": "caller_type_identification",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -400,
                        "y": -200
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "property_owner",
                                "buyer_tenant",
                                "broker",
                                "lender",
                                "general_inquiry"
                            ],
                            "type": "string",
                            "title": "caller_type",
                            "description": "Type of caller based on their commercial real estate needs"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] Are you looking to buy, sell, lease commercial property, or do you have a general inquiry?"
                }
            },
            {
                "name": "caller_name_collection",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -400,
                        "y": -50
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 200,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "caller_name",
                            "description": "Full name of the caller"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[friendly] And may I have your name, please?"
                }
            },
            # BUYER/TENANT BRANCH
            {
                "name": "buyer_property_type_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 100
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "office",
                                "retail",
                                "industrial",
                                "multifamily",
                                "land",
                                "mixed_use",
                                "other"
                            ],
                            "type": "string",
                            "title": "property_type",
                            "description": "Type of commercial property buyer is seeking"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] What type of commercial property are you looking to purchase or lease? Office, retail, industrial, multifamily, or something else?"
                }
            },
            {
                "name": "buyer_location_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 250
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "preferred_locations",
                            "description": "Preferred locations or market areas"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] Which markets or cities are you focusing on for your search?"
                }
            },
            {
                "name": "buyer_budget_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 400
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "budget_range",
                            "description": "Budget range for purchase or lease"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] What's your budget range? For purchase, what price range are you considering? For lease, what's your target rent per square foot?"
                }
            },
            {
                "name": "buyer_size_requirements",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 550
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "size_requirements",
                            "description": "Square footage requirements"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] How much square footage do you need? Any specific size requirements?"
                }
            },
            {
                "name": "buyer_timeline_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 700
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "immediate",
                                "1_to_3_months",
                                "3_to_6_months",
                                "6_plus_months",
                                "unknown"
                            ],
                            "type": "string",
                            "title": "timeline",
                            "description": "Timeline for the transaction"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] What's your timeline for this transaction? When are you looking to close or move in?"
                }
            },
            # PROPERTY OWNER BRANCH
            {
                "name": "owner_property_details",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 100
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "office",
                                "retail",
                                "industrial",
                                "multifamily",
                                "land",
                                "mixed_use",
                                "other"
                            ],
                            "type": "string",
                            "title": "property_type",
                            "description": "Type of commercial property being sold"
                        },
                        {
                            "type": "string",
                            "title": "property_address",
                            "description": "Property address or location"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] I'd be happy to help you with selling your commercial property. What type of property do you own, and where is it located?"
                }
            },
            {
                "name": "owner_property_size",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 250
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "property_size",
                            "description": "Square footage of the property"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] What's the square footage of your property?"
                }
            },
            {
                "name": "owner_asking_price",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 400
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "asking_price",
                            "description": "Desired asking price for the property"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] Do you have a target asking price in mind, or would you like our team to provide a market analysis?"
                }
            },
            {
                "name": "owner_property_status",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 550
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "owner_occupied",
                                "tenant_occupied",
                                "vacant",
                                "partially_occupied"
                            ],
                            "type": "string",
                            "title": "property_status",
                            "description": "Current occupancy status of the property"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] Is the property currently occupied by tenants, owner-occupied, or vacant?"
                }
            },
            {
                "name": "owner_timeline_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 700
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "immediate",
                                "1_to_3_months",
                                "3_to_6_months",
                                "6_plus_months",
                                "unknown"
                            ],
                            "type": "string",
                            "title": "timeline",
                            "description": "Timeline for selling the property"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] What's your timeline for selling? Are you looking to close quickly or do you have flexibility?"
                }
            },
            # BROKER BRANCH
            {
                "name": "broker_details_inquiry",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": 200,
                        "y": 100
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "brokerage_name",
                            "description": "Name of the brokerage firm"
                        },
                        {
                            "type": "string",
                            "title": "license_number",
                            "description": "Real estate license number"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] Great to connect with a fellow broker. What brokerage are you with, and what's your license number?"
                }
            },
            {
                "name": "broker_collaboration_type",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": 200,
                        "y": 250
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "enum": [
                                "co_listing",
                                "referral",
                                "buyer_representation",
                                "joint_venture",
                                "market_information"
                            ],
                            "type": "string",
                            "title": "collaboration_type",
                            "description": "Type of collaboration or partnership"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[enthusiastic] How can we work together? Are you looking for a co-listing opportunity, referral partnership, or something else?"
                }
            },
            {
                "name": "broker_deal_details",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": 200,
                        "y": 400
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 350,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "deal_details",
                            "description": "Details about the specific deal or opportunity"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[thoughtful] Tell me about the specific opportunity. What type of property, location, and deal structure are we looking at?"
                }
            },
            # CONTACT INFORMATION COLLECTION (SHARED)
            {
                "name": "contact_information",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -400,
                        "y": 850
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 250,
                    "temperature": 0.2
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "contact_phone",
                            "description": "Caller's phone number"
                        },
                        {
                            "type": "string",
                            "title": "contact_email",
                            "description": "Caller's email address"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[professional] May I have your phone number and email address so our team can follow up with you?"
                }
            },
            {
                "name": "additional_requirements",
                "type": "conversation",
                "metadata": {
                    "position": {
                        "x": -400,
                        "y": 1000
                    }
                },
                "prompt": "Simply deliver the first message exactly as written. Do not ask any additional questions beyond what's in the first message.",
                "model": {
                    "model": "gpt-4o",
                    "provider": "openai",
                    "maxTokens": 300,
                    "temperature": 0.3
                },
                "voice": {
                    "model": "sonic-3",
                    "voiceId": "57dcab65-68ac-45a6-8480-6c4c52ec1cd1",
                    "provider": "cartesia"
                },
                "transcriber": {
                    "model": "nova-2",
                    "language": "en",
                    "numerals": True,
                    "provider": "deepgram"
                },
                "variableExtractionPlan": {
                    "output": [
                        {
                            "type": "string",
                            "title": "additional_notes",
                            "description": "Any additional requirements or special circumstances"
                        }
                    ]
                },
                "messagePlan": {
                    "firstMessage": "[friendly] Is there anything else I should note about your requirements or preferences?"
                }
            },
            # GOOGLE SHEETS INTEGRATION NODES
            {
                "name": "log_buyer_data",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 1150
                    }
                },
                "tool": {
                    "type": "function",
                    "function": {
                        "name": "log_cre_buyer_data",
                        "description": "Log buyer/tenant data to Google Sheets",
                        "parameters": {
                            "type": "object",
                            "required": ["caller_name", "caller_type", "contact_phone"],
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "description": "Current timestamp"
                                },
                                "caller_name": {
                                    "type": "string",
                                    "description": "Name of the caller"
                                },
                                "caller_type": {
                                    "type": "string",
                                    "description": "Type of caller (buyer_tenant)"
                                },
                                "property_type": {
                                    "type": "string",
                                    "description": "Type of property sought"
                                },
                                "market_location": {
                                    "type": "string",
                                    "description": "Preferred market locations"
                                },
                                "transaction_type": {
                                    "type": "string",
                                    "description": "Purchase or lease"
                                },
                                "size_budget": {
                                    "type": "string",
                                    "description": "Size requirements and budget"
                                },
                                "timeline": {
                                    "type": "string",
                                    "description": "Timeline for transaction"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email address"
                                },
                                "additional_notes": {
                                    "type": "string",
                                    "description": "Additional requirements or notes"
                                },
                                "lead_quality": {
                                    "type": "string",
                                    "description": "Assessment of lead quality"
                                },
                                "call_duration": {
                                    "type": "string",
                                    "description": "Duration of the call"
                                },
                                "call_id": {
                                    "type": "string",
                                    "description": "Unique call identifier"
                                }
                            }
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[professional] Let me log your information in our system.",
                            "blocking": False
                        }
                    ]
                }
            },
            {
                "name": "log_owner_data",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 1150
                    }
                },
                "tool": {
                    "type": "function",
                    "function": {
                        "name": "log_cre_owner_data",
                        "description": "Log property owner data to Google Sheets",
                        "parameters": {
                            "type": "object",
                            "required": ["caller_name", "caller_type", "contact_phone"],
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "description": "Current timestamp"
                                },
                                "caller_name": {
                                    "type": "string",
                                    "description": "Name of the property owner"
                                },
                                "caller_type": {
                                    "type": "string",
                                    "description": "Type of caller (property_owner)"
                                },
                                "property_type": {
                                    "type": "string",
                                    "description": "Type of property being sold"
                                },
                                "property_address": {
                                    "type": "string",
                                    "description": "Property address or location"
                                },
                                "property_size": {
                                    "type": "string",
                                    "description": "Square footage of property"
                                },
                                "asking_price": {
                                    "type": "string",
                                    "description": "Desired asking price"
                                },
                                "property_status": {
                                    "type": "string",
                                    "description": "Current occupancy status"
                                },
                                "timeline": {
                                    "type": "string",
                                    "description": "Timeline for selling"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email address"
                                },
                                "additional_notes": {
                                    "type": "string",
                                    "description": "Additional requirements or notes"
                                },
                                "lead_quality": {
                                    "type": "string",
                                    "description": "Assessment of lead quality"
                                },
                                "call_duration": {
                                    "type": "string",
                                    "description": "Duration of the call"
                                },
                                "call_id": {
                                    "type": "string",
                                    "description": "Unique call identifier"
                                }
                            }
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[professional] Let me record your property details in our system.",
                            "blocking": False
                        }
                    ]
                }
            },
            {
                "name": "log_broker_data",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": 200,
                        "y": 1150
                    }
                },
                "tool": {
                    "type": "function",
                    "function": {
                        "name": "log_cre_broker_data",
                        "description": "Log broker collaboration data to Google Sheets",
                        "parameters": {
                            "type": "object",
                            "required": ["caller_name", "caller_type", "contact_phone"],
                            "properties": {
                                "timestamp": {
                                    "type": "string",
                                    "description": "Current timestamp"
                                },
                                "caller_name": {
                                    "type": "string",
                                    "description": "Name of the broker"
                                },
                                "caller_type": {
                                    "type": "string",
                                    "description": "Type of caller (broker)"
                                },
                                "brokerage_name": {
                                    "type": "string",
                                    "description": "Name of the brokerage firm"
                                },
                                "license_number": {
                                    "type": "string",
                                    "description": "Real estate license number"
                                },
                                "collaboration_type": {
                                    "type": "string",
                                    "description": "Type of collaboration sought"
                                },
                                "deal_details": {
                                    "type": "string",
                                    "description": "Details about the opportunity"
                                },
                                "contact_phone": {
                                    "type": "string",
                                    "description": "Contact phone number"
                                },
                                "contact_email": {
                                    "type": "string",
                                    "description": "Contact email address"
                                },
                                "additional_notes": {
                                    "type": "string",
                                    "description": "Additional requirements or notes"
                                },
                                "lead_quality": {
                                    "type": "string",
                                    "description": "Assessment of opportunity quality"
                                },
                                "call_duration": {
                                    "type": "string",
                                    "description": "Duration of the call"
                                },
                                "call_id": {
                                    "type": "string",
                                    "description": "Unique call identifier"
                                }
                            }
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[professional] Let me add your information to our broker network.",
                            "blocking": False
                        }
                    ]
                }
            },
            # CALL COMPLETION NODES
            {
                "name": "buyer_call_completion",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": -800,
                        "y": 1300
                    }
                },
                "tool": {
                    "type": "endCall",
                    "function": {
                        "name": "complete_buyer_call",
                        "parameters": {
                            "type": "object",
                            "required": [],
                            "properties": {}
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[reassuring] Perfect. Thank you for providing all that information. Our team will review your requirements and follow up within twenty-four hours with relevant properties and next steps. [friendly] Have a great day!",
                            "blocking": True
                        }
                    ]
                }
            },
            {
                "name": "owner_call_completion",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": -100,
                        "y": 1300
                    }
                },
                "tool": {
                    "type": "endCall",
                    "function": {
                        "name": "complete_owner_call",
                        "parameters": {
                            "type": "object",
                            "required": [],
                            "properties": {}
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[reassuring] Excellent. Thank you for considering Summit Commercial Realty for your property sale. Our listing specialist will contact you within twenty-four hours to discuss our marketing strategy and next steps. [friendly] Have a wonderful day!",
                            "blocking": True
                        }
                    ]
                }
            },
            {
                "name": "broker_call_completion",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": 200,
                        "y": 1300
                    }
                },
                "tool": {
                    "type": "endCall",
                    "function": {
                        "name": "complete_broker_call",
                        "parameters": {
                            "type": "object",
                            "required": [],
                            "properties": {}
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[enthusiastic] Great connecting with you! Our partnership team will reach out within twenty-four hours to discuss this opportunity and how we can work together. [friendly] Looking forward to collaborating!",
                            "blocking": True
                        }
                    ]
                }
            },
            {
                "name": "call_declined",
                "type": "tool",
                "metadata": {
                    "position": {
                        "x": -700,
                        "y": -200
                    }
                },
                "tool": {
                    "type": "endCall",
                    "function": {
                        "name": "handle_call_declined",
                        "parameters": {
                            "type": "object",
                            "required": [],
                            "properties": {}
                        }
                    },
                    "messages": [
                        {
                            "type": "request-start",
                            "content": "[friendly] I understand you're busy. I'll have our team reach out at a more convenient time. Have a great day!",
                            "blocking": True
                        }
                    ]
                }
            }
        ],
        "edges": [
            # INITIAL ROUTING
            {
                "from": "introduction",
                "to": "caller_type_identification",
                "condition": {
                    "type": "ai",
                    "prompt": "if user responds positively or shows interest in continuing the conversation"
                }
            },
            {
                "from": "introduction",
                "to": "call_declined",
                "condition": {
                    "type": "ai",
                    "prompt": "if call_consent is no or later, or user wants to end the call"
                }
            },
            {
                "from": "caller_type_identification",
                "to": "caller_name_collection",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides any type of inquiry or continues the conversation"
                }
            },
            
            # BUYER/TENANT BRANCH
            {
                "from": "caller_name_collection",
                "to": "buyer_property_type_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is buyer_tenant or caller mentions buying, purchasing, leasing, or looking for property"
                }
            },
            {
                "from": "buyer_property_type_inquiry",
                "to": "buyer_location_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides property type information"
                }
            },
            {
                "from": "buyer_location_inquiry",
                "to": "buyer_budget_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides location information"
                }
            },
            {
                "from": "buyer_budget_inquiry",
                "to": "buyer_size_requirements",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides budget information"
                }
            },
            {
                "from": "buyer_size_requirements",
                "to": "buyer_timeline_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides size requirements"
                }
            },
            {
                "from": "buyer_timeline_inquiry",
                "to": "contact_information",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides timeline information"
                }
            },
            
            # PROPERTY OWNER BRANCH
            {
                "from": "caller_name_collection",
                "to": "owner_property_details",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is property_owner or caller mentions selling, listing, or owning property"
                }
            },
            {
                "from": "owner_property_details",
                "to": "owner_property_size",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides property details"
                }
            },
            {
                "from": "owner_property_size",
                "to": "owner_asking_price",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides property size information"
                }
            },
            {
                "from": "owner_asking_price",
                "to": "owner_property_status",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides pricing information"
                }
            },
            {
                "from": "owner_property_status",
                "to": "owner_timeline_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides property status information"
                }
            },
            {
                "from": "owner_timeline_inquiry",
                "to": "contact_information",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides timeline information"
                }
            },
            
            # BROKER BRANCH
            {
                "from": "caller_name_collection",
                "to": "broker_details_inquiry",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is broker or caller mentions being a broker, agent, or representing another brokerage"
                }
            },
            {
                "from": "broker_details_inquiry",
                "to": "broker_collaboration_type",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides brokerage information"
                }
            },
            {
                "from": "broker_collaboration_type",
                "to": "broker_deal_details",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides collaboration type"
                }
            },
            {
                "from": "broker_deal_details",
                "to": "contact_information",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides deal details"
                }
            },
            
            # SHARED CONTACT AND COMPLETION FLOW
            {
                "from": "contact_information",
                "to": "additional_requirements",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller provides contact information"
                }
            },
            
            # GOOGLE SHEETS LOGGING BRANCHES
            {
                "from": "additional_requirements",
                "to": "log_buyer_data",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is buyer_tenant"
                }
            },
            {
                "from": "additional_requirements",
                "to": "log_owner_data",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is property_owner"
                }
            },
            {
                "from": "additional_requirements",
                "to": "log_broker_data",
                "condition": {
                    "type": "ai",
                    "prompt": "if caller_type is broker"
                }
            },
            
            # CALL COMPLETION BRANCHES
            {
                "from": "log_buyer_data",
                "to": "buyer_call_completion",
                "condition": {
                    "type": "ai",
                    "prompt": "after logging buyer data"
                }
            },
            {
                "from": "log_owner_data",
                "to": "owner_call_completion",
                "condition": {
                    "type": "ai",
                    "prompt": "after logging owner data"
                }
            },
            {
                "from": "log_broker_data",
                "to": "broker_call_completion",
                "condition": {
                    "type": "ai",
                    "prompt": "after logging broker data"
                }
            }
        ],
        "globalPrompt": """## System Identity
You are Michael, a professional AI assistant for Summit Commercial Realty, a mid-tier commercial brokerage specializing in office, retail, industrial, and multifamily properties. You are knowledgeable, professional, and efficient in qualifying leads and understanding commercial real estate needs.

## Core Objectives
1. Qualify all inbound callers professionally (property owners, buyers, tenants, brokers, lenders)
2. Identify caller type early and route to appropriate conversation path
3. Gather comprehensive information specific to each caller type
4. Maintain a professional yet warm tone with natural expressiveness
5. Capture complete caller data and log to appropriate Google Sheets
6. Handle all inquiries with CRE market knowledge

## Communication Guidelines - Cartesia Sonic 3 Expressiveness

### Using Cartesia Sonic 3 Emotional Expressions
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

## Caller-Specific Conversation Paths

### For Buyers/Tenants:
1. Property type preferences (office, retail, industrial, etc.)
2. Preferred locations and markets
3. Budget range (purchase price or lease rate)
4. Size requirements (square footage)
5. Timeline for transaction
6. Contact information and additional requirements

### For Property Owners:
1. Property details (type, address, location)
2. Property size (square footage)
3. Asking price expectations or need for market analysis
4. Current property status (occupied, vacant, etc.)
5. Timeline for selling
6. Contact information and additional requirements

### For Brokers:
1. Brokerage details (firm name, license number)
2. Collaboration type (co-listing, referral, joint venture)
3. Specific deal details and opportunity
4. Contact information and additional requirements

## Data Collection & Google Sheets Integration
- Automatically log all collected data to appropriate Google Sheets
- Buyer/Tenant data goes to buyer sheet
- Property Owner data goes to owner sheet  
- Broker data goes to broker collaboration sheet
- Include timestamp, call duration, call ID, and lead quality assessment

## Professional Standards
- Respect caller's time and be efficient
- Use commercial real estate terminology appropriately
- Be honest about capabilities and market coverage
- Maintain Summit Commercial Realty's reputation for professionalism
- Set clear expectations for follow-up within 24 hours

## Success Criteria
- Correctly identify caller type in 95%+ of calls
- Gather complete contact information in 90%+ of calls
- Route to appropriate conversation path based on caller type
- Maintain professional tone with natural expressiveness throughout
- Capture caller-specific details for meaningful follow-up
- Average call duration: 3-5 minutes

## Key Differentiators by Caller Type
- **Buyers/Tenants**: Focus on requirements, preferences, and finding suitable properties
- **Property Owners**: Focus on property details, market positioning, and selling strategy
- **Brokers**: Focus on collaboration opportunities and partnership potential

Remember: You represent Summit Commercial Realty professionally. Every call is an opportunity to create a positive impression and generate quality leads or partnerships for our brokerage team. Adapt your approach based on the caller type while maintaining consistent professionalism."""
    }