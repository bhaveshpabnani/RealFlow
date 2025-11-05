# RealFlow CRE Workflow System

**Created by: Bhavesh Nareshkumar Pabnani**

A production-grade VAPI-powered voice agent system for commercial real estate lead generation and qualification. This system provides intelligent call routing, comprehensive data collection, and seamless Google Sheets integration for CRE professionals.

## 🏗️ System Architecture

RealFlow implements a sophisticated voice agent system with:
- **Intelligent Call Routing**: Separate conversation paths for Buyers/Tenants, Property Owners, and Brokers
- **Professional Voice Agent**: Cartesia Sonic 3 (Aria Voice) with natural emotional expressions
- **Comprehensive Data Collection**: Structured data extraction and Google Sheets logging
- **Production-Ready APIs**: FastAPI-based endpoints for workflow and call management
- **Twilio Integration**: Professional phone number with SIP trunk configuration

## 🚀 Key Features

### Voice Agent Capabilities
- **Multi-Caller Type Support**: Dedicated conversation flows for different caller types
- **Natural Conversations**: One question per turn with professional CRE terminology
- **Emotional Intelligence**: Cartesia Sonic 3 expressions for warm, professional interactions
- **Comprehensive Lead Qualification**: 3-5 minute calls with 90%+ contact capture rate

### Data Management
- **Google Sheets Integration**: Automatic logging to separate sheets (Buyer, Owner, Broker)
- **Structured Data Extraction**: VAPI-powered variable extraction from conversations
- **Real-time Analytics**: Call statistics and lead quality assessment
- **Complete Audit Trail**: Timestamps, call duration, and call ID tracking

### Technical Infrastructure
- **VAPI Integration**: Workflow builder, assistant management, and call orchestration
- **Twilio Phone System**: Professional phone number with elastic SIP trunk
- **Railway Deployment**: Production-ready cloud hosting configuration
- **RESTful APIs**: Comprehensive endpoints for system management

## 📋 Implementation Details

### VAPI Configuration
- ✅ **Twilio Phone Number**: Configured with VAPI URL and elastic SIP trunk
- ✅ **VAPI Assistant**: Cartesia Sonic 3 (Aria Voice) configuration
- ✅ **Workflow Builder**: Dynamic workflows with caller-specific branching
- ✅ **Google Sheets Tools**: OAuth service account integration
- ✅ **Structured Data Extraction**: Variable extraction for lead qualification

### Google Sheets Setup
- ✅ **Separate Sheets**: Owner, Customer (Buyer/Tenant), Broker information
- ✅ **Service Account**: Google OAuth credentials with sheet sharing
- ✅ **Automated Logging**: Real-time data capture from voice calls
- ✅ **Comprehensive Fields**: 14-17 data points per caller type

### System Components
- ✅ **FastAPI Endpoints**: Create/list assistants, tools, workflows
- ✅ **Call Management**: Initiate calls, track status, log details
- ✅ **Webhook Integration**: NGROK-based local testing and VAPI integration
- ✅ **Modular Architecture**: Separate Assistant and Workflow implementations

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- VAPI Account with API key
- Google Cloud Service Account
- Twilio Account (optional, for phone number)

### Local Development

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd RealFlow
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

4. **Google Sheets Setup**
   ```bash
   # Place your Google service account credentials
   cp your-credentials.json credentials.json
   ```

5. **Run Development Server**
   ```bash
   python run.py
   # Or directly: python -m uvicorn src.workflow.main:app --reload
   ```

### Production Deployment (Railway)

1. **Deploy to Railway**
   ```bash
   # Connect your GitHub repository to Railway
   # Railway will automatically detect railway.toml configuration
   ```

2. **Environment Variables**
   Set these in Railway dashboard:
   ```
   VAPI_API_KEY=your_vapi_api_key
   VAPI_PHONE_NUMBER=your_phone_number
   VAPI_PHONE_NUMBER_ID=your_phone_number_id
   GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
   GOOGLE_CREDENTIALS_JSON=your_service_account_json
   ```

3. **Domain Configuration**
   ```
   # Railway provides automatic HTTPS domain
   # Update VAPI webhook URLs to point to your Railway domain
   ```

## 🔧 Configuration

### Environment Variables

```bash
# VAPI Configuration
VAPI_API_KEY=your_vapi_api_key
VAPI_PHONE_NUMBER=+1234567890
VAPI_PHONE_NUMBER_ID=your_phone_number_id

# Google Sheets
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id
GOOGLE_CREDENTIALS_JSON={"type": "service_account", ...}

# Voice Settings
VOICE_PROVIDER=cartesia
VOICE_ID=57dcab65-68ac-45a6-8480-6c4c52ec1cd1  # Cartesia Sonic 3
VOICE_MODEL=sonic-3

# Model Settings
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4o
MODEL_TEMPERATURE=0.3
```

### Google Sheets Structure

#### Buyer/Tenant Sheet Columns
- Timestamp, Caller Name, Caller Type, Property Type, Market Location
- Transaction Type, Size/Budget, Timeline, Contact Phone, Contact Email
- Additional Notes, Lead Quality, Call Duration, Call ID
- Preferred Locations, Size Requirements, Budget Range

#### Property Owner Sheet Columns
- Timestamp, Caller Name, Caller Type, Property Type, Market Location
- Transaction Type, Size/Budget, Timeline, Contact Phone, Contact Email
- Additional Notes, Lead Quality, Call Duration, Call ID
- Property Address, Property Size, Asking Price, Property Status

#### Broker Sheet Columns
- Timestamp, Caller Name, Caller Type, Property Type, Market Location
- Transaction Type, Size/Budget, Timeline, Contact Phone, Contact Email
- Additional Notes, Lead Quality, Call Duration, Call ID
- Brokerage Name, License Number, Collaboration Type, Deal Details

## 📡 API Endpoints

### Workflow Management
```
POST   /workflow/create              # Create new workflow
GET    /workflow/workflows           # List all workflows
POST   /workflow/call/initiate       # Initiate outbound call
GET    /workflow/calls               # List recent calls
GET    /workflow/health              # Health check
```

### Assistant Management
```
POST   /assistant/create             # Create VAPI assistant
GET    /assistant/list               # List assistants
POST   /assistant/call               # Initiate call via assistant
GET    /assistant/calls              # Get call history
POST   /webhook                      # VAPI webhook endpoint
```

### Data & Analytics
```
GET    /workflow/statistics          # Call statistics
GET    /workflow/calls/recent        # Recent calls by sheet
POST   /workflow/test/sheets         # Test Google Sheets logging
```

## 🎯 Workflow Architecture

### Conversation Flow
1. **Introduction**: Professional greeting and consent
2. **Caller Type Identification**: Route to appropriate branch
3. **Caller-Specific Information Gathering**:
   - **Buyers/Tenants**: Property requirements, location, budget, timeline
   - **Property Owners**: Property details, pricing, status, timeline
   - **Brokers**: Brokerage info, collaboration type, deal details
4. **Contact Information**: Phone and email collection
5. **Additional Requirements**: Special notes and preferences
6. **Google Sheets Logging**: Automatic data capture
7. **Professional Completion**: Tailored closing message

### Voice Agent Features
- **Cartesia Sonic 3 Expressions**: `[friendly]`, `[professional]`, `[thoughtful]`, `[reassuring]`
- **Natural Conversation**: One question per turn methodology
- **CRE Terminology**: Professional commercial real estate language
- **Lead Qualification**: Comprehensive data collection for follow-up

## 🧪 Testing

### Local Testing
```bash
# Test workflow creation
curl -X POST "http://localhost:8001/workflow/create"

# Test call initiation
curl -X POST "http://localhost:8001/workflow/call/initiate" \
  -H "Content-Type: application/json" \
  -d '{"customer_phone": "+1234567890", "workflow_id": "workflow_id"}'

# Test Google Sheets logging
curl -X POST "http://localhost:8001/workflow/test/sheets"
```

### VAPI Dashboard Testing
1. Access VAPI dashboard
2. Navigate to created workflows
3. Test conversation flows
4. Verify Google Sheets integration
5. Monitor call analytics

## 📊 Performance Metrics

### Target KPIs
- **Caller Type Identification**: 95%+ accuracy
- **Contact Information Capture**: 90%+ completion rate
- **Call Duration**: 3-5 minutes average
- **Lead Quality**: Comprehensive data for broker follow-up
- **System Uptime**: 99.9% availability

### Monitoring
- Real-time call statistics via `/workflow/statistics`
- Google Sheets data validation
- VAPI dashboard analytics
- Railway deployment metrics

## 🔒 Security & Compliance

### Data Protection
- Google OAuth service account authentication
- Environment variable encryption
- HTTPS-only communication
- No sensitive data in logs

### VAPI Security
- API key authentication
- Webhook signature validation
- Rate limiting and retry logic
- Secure credential storage

## 🚀 Deployment Options

### Railway (Recommended)
1. **Connect Repository**: Link your GitHub repository to Railway
2. **Environment Variables**: Set all required variables in Railway dashboard
3. **Automatic Deployment**: Railway detects `railway.toml` and deploys automatically
4. **Custom Domain**: Railway provides HTTPS domain or use custom domain

### Alternative Platforms
- **Heroku**: Use `Procfile` configuration
- **AWS/GCP**: Container deployment with Docker
- **DigitalOcean**: App Platform deployment

### Railway Deployment Steps
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Initialize project
railway init

# 4. Set environment variables
railway variables set VAPI_API_KEY=your_key
railway variables set GOOGLE_SHEETS_SPREADSHEET_ID=your_id
# ... set all required variables

# 5. Deploy
railway up
```

## 📞 Support & Maintenance

### Monitoring
- Railway dashboard for deployment health
- VAPI dashboard for call analytics
- Google Sheets for data validation
- API endpoint health checks

### Troubleshooting
- Check environment variables in Railway dashboard
- Verify Google Sheets permissions
- Validate VAPI API key and phone number configuration
- Review webhook configurations and logs

### Common Issues
1. **Google Sheets Access**: Ensure service account has edit permissions
2. **VAPI Webhooks**: Update webhook URLs after deployment
3. **Environment Variables**: Verify all required variables are set
4. **Phone Number**: Confirm Twilio number is properly configured

## 🎉 Success Metrics

This implementation successfully delivers:
- ✅ **Professional Voice Agent**: Cartesia Sonic 3 with natural expressions
- ✅ **Intelligent Call Routing**: Separate paths for different caller types
- ✅ **Comprehensive Data Collection**: 14-17 fields per caller type
- ✅ **Google Sheets Integration**: Real-time data logging
- ✅ **Production-Ready APIs**: FastAPI with comprehensive endpoints
- ✅ **Railway Deployment**: Cloud-ready configuration
- ✅ **Complete Testing**: VAPI dashboard and API validation

## 📋 Project Structure

```
RealFlow/
├── src/
│   ├── assistant/           # Assistant-based implementation
│   │   ├── api/            # FastAPI routes
│   │   ├── services/       # Core services
│   │   ├── tools/          # Management tools
│   │   └── models.py       # Data models
│   └── workflow/           # Workflow-based implementation
│       ├── services/       # Workflow services
│       ├── models.py       # Workflow models
│       └── main.py         # Application entry
├── credentials.json        # Google service account
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── railway.toml          # Railway deployment config
├── Procfile              # Process configuration
└── README.md             # This file
```

## 📝 License

This project is proprietary software developed for commercial real estate lead generation.

---

**Created by Bhavesh Nareshkumar Pabnani**  
*Professional VAPI Voice Agent System for Commercial Real Estate*

## 🔗 Quick Links

- **VAPI Dashboard**: [https://dashboard.vapi.ai](https://dashboard.vapi.ai)
- **Railway Dashboard**: [https://railway.app](https://railway.app)
- **Google Cloud Console**: [https://console.cloud.google.com](https://console.cloud.google.com)
- **API Documentation**: Visit `/docs` when server is running