# AI Integration Guide for Business Risk Analysis

## Overview

This guide explains how to integrate your AI service with the Business Risk Analysis platform. The system sends company data, documents, and news to your AI service and stores the results.

## Quick Start

### Environment Variable
Set your AI service endpoint:
```bash
export AI_ENDPOINT_URL="https://your-ai-service.com/analyze"
```

### API Endpoint
**URL**: `POST /api/companies/{company_id}/analyse`

This endpoint sends data to your AI service and stores the results.

## Request Format

### General Analysis
```bash
curl -X POST "http://localhost:5001/api/companies/company_123/analyse" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Dynamic Risk Analysis
```bash
curl -X POST "http://localhost:5001/api/companies/company_123/analyse" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_description": "New GDPR regulations require immediate data processing changes",
    "risk_context": "Additional context about the risk scenario",
    "risk_type": "regulatory"
  }'
```

## Data Structure Sent to Your AI Service

Your AI service will receive this JSON payload:

```json
{
  "company_info": {
    "name": "Tesla Inc",
    "context": ["Electric vehicle manufacturer", "Global operations"],
    "documents": [
      {
        "file_name": "master_service_agreement.pdf",
        "content": "This Master Service Agreement (MSA) is entered into...",
        "file_type": "pdf"
      }
    ]
  },
  "news_data": {
    "articles_summary": [
      {
        "title": "Oil prices surge as Iran tensions escalate",
        "description": "Global oil markets react to rising tensions...",
        "content": "Oil prices surged to their highest level...",
        "url": "https://www.reuters.com/business/energy/...",
        "source": "Reuters",
        "date": "2024-01-15T10:00:00Z",
        "sentiment": "negative"
      }
    ]
  },
  "risk_scenario": {
    "description": "New GDPR regulations require immediate data processing changes",
    "context": "Additional context about the risk scenario",
    "type": "regulatory",
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```

**Note**: The `risk_scenario` field is only included for dynamic risk analysis requests.

## Expected Response from Your AI Service

Your AI service should return a JSON response. The format is flexible - return whatever structure makes sense for your analysis.

### Example Response for General Analysis
```json
{
  "risk_factors": [
    {
      "severity": "Low",
      "risk_type": "Reputational Risk",
      "specific_event": "Middle East War",
      "affected_contracts": "contract.pdf",
      "affected_clauses": "Clause 1.1",
      "narrative": {
        "solutions_in_contract": "The contract does have a clause that addresses this risk. 16.1",
        "alternative_mitigation_strategies": "Do xyz to mitigate the risk.",
        "monitoring_tasks": "Monitor the risk and report to the board every 3 months."
      }
    }
  ],
  "available_data": {
    "context_items": ["Company context information"],
    "document_count": 3,
    "content_available": true,
    "news_available": true
  }
}
```

### Example Response for Dynamic Risk Analysis
```json
{
  "risk_analysis": {
    "scenario": "New GDPR regulations require immediate data processing changes",
    "risk_level": "High",
    "impact_assessment": "This regulatory risk represents an existential threat to company operations...",
    "affected_areas": [
      "Contractual obligations and SLA compliance",
      "Customer relationship management and retention",
      "Financial stability and cash flow"
    ]
  },
  "news_analysis": {
    "articles_found": 15,
    "negative_sentiment_ratio": 0.4,
    "trending_topics": ["GDPR compliance", "Data protection", "Regulatory changes"],
    "market_context": "Found 15 relevant articles with 6 showing negative sentiment"
  },
  "recommendations": [
    "Immediate Legal Response: Engage outside counsel specializing in data protection...",
    "Customer Communication Strategy: Develop a comprehensive communication plan...",
    "Compliance Planning: Immediately initiate GDPR compliance assessment..."
  ],
  "next_steps": [
    "Executive Crisis Management: Convene an emergency board meeting within 24 hours...",
    "Financial Risk Mitigation: Immediately review all insurance policies...",
    "Regulatory and Compliance Review: Conduct immediate review of all regulatory obligations..."
  ],
  "ai_confidence": 0.92,
  "analysis_timestamp": "2024-01-15T12:00:00Z"
}
```

## Integration Example

### Python AI Service
```python
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    
    # Extract data
    company_name = data['company_info']['name']
    documents = data['company_info']['documents']
    news_articles = data['news_data']['articles_summary']
    
    # Check if this is a dynamic risk analysis
    is_dynamic_risk = 'risk_scenario' in data
    
    if is_dynamic_risk:
        risk_description = data['risk_scenario']['description']
        risk_type = data['risk_scenario']['type']
        
        # Your AI analysis logic here
        result = {
            "risk_analysis": {
                "scenario": risk_description,
                "risk_level": "High",
                "impact_assessment": f"This {risk_type} risk could significantly impact {company_name}.",
                "affected_areas": ["Operations", "Compliance", "Finance"]
            },
            "recommendations": [
                "Immediate action required",
                "Review all contracts",
                "Consult legal counsel"
            ],
            "ai_confidence": 0.85
        }
    else:
        # General analysis
        result = {
            "risk_factors": [
                {
                    "severity": "Medium",
                    "risk_type": "Operational Risk",
                    "specific_event": "Supply Chain Disruption",
                    "affected_contracts": "supplier_agreement.pdf",
                    "affected_clauses": "Force Majeure",
                    "narrative": {
                        "solutions_in_contract": "Contract includes force majeure provisions.",
                        "alternative_mitigation_strategies": "Diversify suppliers and increase inventory.",
                        "monitoring_tasks": "Monitor supplier performance monthly."
                    }
                }
            ],
            "available_data": {
                "context_items": data['company_info']['context'],
                "document_count": len(documents),
                "content_available": True,
                "news_available": len(news_articles) > 0
            }
        }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5002)
```

## Requirements

### Performance
- **Response Time**: <30 seconds
- **Payload Size**: Handle up to 50MB of document content
- **Availability**: 99.9% uptime

### Error Handling
- Return HTTP 200 with JSON response on success
- Return HTTP 500 with error message on failure
- Handle malformed requests gracefully

### Security
- Use HTTPS in production
- Validate input data
- Implement rate limiting if needed

## Testing

Test your AI service with:

1. **General Analysis**: Send empty payload `{}`
2. **Dynamic Risk**: Send risk scenario data
3. **Edge Cases**: Empty documents, missing news
4. **Large Payloads**: Many documents and articles

## What Happens Next

1. **Data Sent**: Your AI service receives company data, documents, and news
2. **Analysis Performed**: Your AI service analyzes the data
3. **Results Stored**: The platform stores your analysis results in the database
4. **Response Returned**: Results are returned to the user with an analysis ID

The analysis results are stored in the database and can be retrieved later using the analysis ID.

---

**Note**: This integration is simple and flexible. Your AI service can return any JSON structure that makes sense for your analysis. 