# RealFlow CRE Workflow System

A standalone, dynamic VAPI workflow system for commercial real estate lead generation and qualification.

## 🚀 Quick Start

### Run the Workflow System

```bash
# Development mode (port 8001)
poetry run workflow-dev

# Production mode
poetry run workflow-start

# Or directly with Python
poetry run python -m workflow.main
```

### CLI Commands

```bash
# Show available commands
poetry run workflow-cli --help

# Test connections
poetry run workflow-cli test-connection

# Show configuration
poetry run workflow-cli config-info

# Create a workflow
poetry run workflow-cli create-workflow --caller-type property_owner --name "Property Owner Flow"

# List workflows
poetry run workflow-cli list-workflows

# Initiate a test call
poetry run workflow-cli initiate-call +1234567890 --caller-type property_owner

# Check call status
poetry run workflow-cli call-status <call-id>

# Setup complete system
poetry run workflow-cli setup-system <spreadsheet-id> <phone-number>
```

## 📁 Module Structure

```
src/workflow/
├── __init__.py              # Package initialization
├── main.py                  # FastAPI application entry point
├── cli.py                   # Command line interface
├── config.py                # Configuration management
├── models.py                # Data models and enums
├── node_factory.py          # Creates workflow nodes
├── edge_generator.py        # Creates routing edges
├── workflow_builder.py      # Orchestrates workflow creation
├── vapi_client.py           # VAPI API client
├── cre_workflow.py          # Main workflow orchestrator
├── api_routes.py            # FastAPI routes
├── setup_tools.py           # Setup and configuration tools
└── services/
    ├── __init__.py
    └── sheets_service.py     # Google Sheets integration
```

## 🌐 API Endpoints

The workflow system runs on port 8001 (different from assistant on 8000):

```
GET  /                       # System information
GET  /workflow/health        # Health check
POST /workflow/create        # Create workflow
POST /workflow/call/initiate # Initiate call
GET  /workflow/call/{id}/status # Get call status
POST /workflow/webhook/vapi  # VAPI webhook handler
GET  /workflow/workflows     # List workflows
GET  /workflow/calls         # List calls
GET  /workflow/caller-types  # Available caller types
GET  /workflow/stats/calls   # Call statistics
GET  /workflow/stats/recent/{sheet} # Recent calls by type
POST /workflow/sheets/test-log # Test Google Sheets logging
POST /workflow/test/workflow # Test workflow creation
POST /workflow/test/call     # Test call initiation
```

## 🎯 Key Features

### 1. Independent Operation
- Runs separately from the assistant system
- Own FastAPI application on port 8001
- Independent configuration and dependencies
- Can be deployed separately

### 2. Dynamic Workflow Creation
- Creates workflows based on caller type
- Adapts to missing information requirements
- One question per conversation turn
- Conditional routing based on responses

### 3. Comprehensive CLI
- Full command-line interface for management
- Test connections and configurations
- Create workflows and initiate calls
- Monitor system health and performance

### 4. Professional CRE Focus
- Commercial real estate terminology
- Lead qualification and scoring
- Caller type identification
- Professional conversation flows

### 5. Google Sheets Integration
- Automatic data logging by caller type
- Real-time statistics and reporting
- Test logging capabilities
- Connection health monitoring

## 🔧 Configuration

### Environment Variables

```env
# VAPI Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_BASE_URL=https://api.vapi.ai
VAPI_PHONE_NUMBER_ID=your_phone_number_id
VAPI_PHONE_NUMBER=+1234567890

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_SHEETS_CREDENTIALS_PATH=credentials.json

# Voice Settings (optional)
CARTESIA_VOICE_ID=sonic
CARTESIA_MODEL_ID=sonic-english
ELEVENLABS_VOICE_ID=fallback_voice_id
ELEVENLABS_MODEL_ID=fallback_model_id
```

### Voice Provider Priority
1. Cartesia (if CARTESIA_VOICE_ID is set)
2. ElevenLabs (if ELEVENLABS_VOICE_ID is set)
3. Default values

## 🧪 Testing

### Connection Tests
```bash
# Test all connections
poetry run workflow-cli test-connection

# Health check via API
curl http://localhost:8001/workflow/health
```

### Workflow Tests
```bash
# Test workflow creation
curl -X POST http://localhost:8001/workflow/test/workflow

# Test call initiation
curl -X POST http://localhost:8001/workflow/test/call
```

### Google Sheets Tests
```bash
# Test sheets logging
curl -X POST http://localhost:8001/workflow/sheets/test-log

# Get call statistics
curl http://localhost:8001/workflow/stats/calls
```

## 📊 Monitoring

### System Health
- VAPI connection status
- Google Sheets connectivity
- Workflow creation performance
- Call success rates

### Call Analytics
- Total calls by type
- Recent call activity
- Lead quality distribution
- Response time metrics

### Data Quality
- Field completion rates
- Conversation flow efficiency
- Error rates and types

## 🔄 Workflow Types

### Property Owner Workflow
- Collects property details, pricing, and motivation
- Routes to owner-specific Google Sheet
- Focuses on listing and selling information

### Buyer/Tenant Workflow
- Gathers requirements and preferences
- Routes to customer Google Sheet
- Emphasizes needs and timeline

### Broker Workflow
- Professional collaboration focus
- Routes to broker Google Sheet
- Handles referrals and partnerships

### Lender Workflow
- Financing capabilities and terms
- Routes to lender Google Sheet
- Loan products and requirements

### General Inquiry Workflow
- Service information and interest
- Routes to general Google Sheet
- Broad information gathering

## 🚀 Deployment

### Standalone Deployment
```bash
# Install dependencies
poetry install

# Run in production
poetry run workflow-start
```

### Docker Deployment
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install poetry && poetry install --no-dev
EXPOSE 8001
CMD ["poetry", "run", "workflow-start"]
```

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env

# Setup system
poetry run workflow-cli setup-system <spreadsheet-id> <phone-number>
```

## 🔒 Security

### API Security
- Environment-based configuration
- Secure API key management
- Request validation and sanitization
- Error handling without data exposure

### Data Protection
- Encrypted HTTPS communication
- Google Sheets access controls
- Minimal data collection
- Audit logging capabilities

## 📈 Performance

### Optimization Features
- Async/await throughout
- Connection pooling
- Efficient VAPI API usage
- Caching where appropriate

### Scalability
- Stateless design
- Horizontal scaling ready
- Database-free operation
- Cloud deployment friendly

## 🤝 Integration

### With Assistant System
- Independent operation
- Shared environment variables
- Compatible data formats
- Complementary functionality

### With External Systems
- VAPI platform integration
- Google Sheets API
- Webhook-based communication
- RESTful API design

## 📚 Development

### Adding New Caller Types
1. Update `CallerCategory` enum in `models.py`
2. Add node creation in `node_factory.py`
3. Update routing in `edge_generator.py`
4. Add field mappings in `config.py`

### Extending Functionality
1. Add new API routes in `api_routes.py`
2. Extend CLI commands in `cli.py`
3. Update configuration in `config.py`
4. Add tests and documentation

### Testing Changes
```bash
# Run connection tests
poetry run workflow-cli test-connection

# Test API endpoints
curl http://localhost:8001/workflow/health

# Validate configuration
poetry run workflow-cli config-info
```

---

**RealFlow CRE Workflow System** - Professional, scalable, and intelligent voice workflows for commercial real estate lead generation.