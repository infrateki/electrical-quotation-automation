# ProQuote - Electrical Quotation Automation System

An AI-powered electrical quotation automation system built with multi-agent orchestration using LangGraph.

## 🚀 Features

- **Multi-Agent Architecture**: Leverages specialized AI agents for different aspects of quotation generation
- **LangGraph Orchestration**: Coordinates agent workflows for efficient processing
- **Async Processing**: Background task execution for non-blocking operations
- **RESTful API**: FastAPI-powered endpoints for full quotation lifecycle management
- **Comprehensive Testing**: Unit tests, integration tests, and test coverage >95%

## 📋 System Architecture

### Agents

1. **Simple Agents** (Template-based)
   - `HeaderAgent`: Generates quotation headers with auto-numbering
   - `FooterAgent`: Manages terms, conditions, and signature blocks
   - `CompanyInfoAgent`: Handles company branding and contact details

2. **Orchestrator**
   - `QuotationOrchestrator`: LangGraph-based workflow coordinator
   - Manages agent execution order and error handling
   - Tracks execution logs and state management

### API Endpoints

- `POST /api/v1/quotations/` - Create new quotation
- `GET /api/v1/quotations/` - List quotations with filtering
- `GET /api/v1/quotations/{id}` - Get quotation details
- `PATCH /api/v1/quotations/{id}` - Update quotation
- `DELETE /api/v1/quotations/{id}` - Delete quotation
- `POST /api/v1/quotations/{id}/generate` - Trigger AI generation
- `GET /api/v1/quotations/{id}/status` - Check generation status
- `GET /api/v1/quotations/{id}/document` - Get formatted document

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/infrateki/electrical-quotation-automation.git
cd electrical-quotation-automation
```

2. Install dependencies:
```bash
pip install -e .
```

3. Run the application:
```bash
uvicorn api.main:app --reload
```

## 📖 Usage

### Create a Quotation

```python
import requests

# Create quotation
response = requests.post(
    "http://localhost:8000/api/v1/quotations/",
    json={
        "company_name": "ProQuote Electrical Ltd",
        "prepared_by": "John Smith",
        "client_name": "ABC Corporation",
        "project_name": "Office Renovation"
    }
)
quotation = response.json()

# Generate using AI agents
response = requests.post(
    f"http://localhost:8000/api/v1/quotations/{quotation['id']}/generate"
)

# Check status
status = requests.get(
    f"http://localhost:8000/api/v1/quotations/{quotation['id']}/status"
).json()

# Get formatted document
document = requests.get(
    f"http://localhost:8000/api/v1/quotations/{quotation['id']}/document"
).json()
```

## 🧪 Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=agents --cov=shared --cov=api
```

## 📁 Project Structure

```
electrical-quotation-automation/
├── agents/
│   ├── orchestrator/        # LangGraph orchestration
│   ├── simple_agents/       # Template-based agents
│   ├── workflow_agents/     # Logic-based agents (future)
│   └── advanced_agents/     # AI-powered agents (future)
├── api/
│   ├── routes/             # API endpoints
│   ├── middleware/         # Request processing
│   └── dependencies/       # Dependency injection
├── shared/
│   ├── models/            # Data models and schemas
│   ├── data_access/       # Database operations
│   ├── utils/             # Utility functions
│   └── exceptions/        # Custom exceptions
├── services/
│   ├── pricing_apis/      # External pricing services
│   ├── compliance_engine/ # Compliance checks
│   └── notification/      # Notification services
└── tests/
    ├── unit/              # Unit tests
    ├── integration/       # Integration tests
    └── fixtures/          # Test data

```

## 🔄 Current Status

### ✅ Completed
- Project structure and setup
- Base agent framework
- Simple agents (Header, Footer, CompanyInfo)
- LangGraph orchestrator
- FastAPI endpoints
- Async processing
- Comprehensive testing

### 🚧 In Progress
- Database persistence (SQLAlchemy)
- LineItemsAgent for quotation items
- PricingAgent for calculations

### 📅 Planned
- Advanced AI agents
- PDF generation
- Email notifications
- User authentication
- Web UI

## 🤝 Contributing

This project follows a multi-agent development approach. See `CLAUDE.md` for agent coordination guidelines.

## 📝 License

MIT License - see LICENSE file for details.

## 🏢 About

ProQuote is developed by INFRATEK for automating electrical quotation generation using cutting-edge AI technology.