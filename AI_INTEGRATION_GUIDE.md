git# AI Integration Guide for Business Risk Analysis

## Overview

This guide provides comprehensive documentation for integrating AI services with the Business Risk Analysis platform. The system offers a unified analysis endpoint that can handle both general company risk assessment and dynamic risk scenario analysis.

## Quick Start

### Base URL
- **Development**: `http://localhost:5001`
- **Production**: `https://your-production-domain.com`

### Unified Analysis Endpoint
**URL**: `POST /api/companies/{company_id}/analyse`

This single endpoint handles both general and dynamic risk analysis based on the request payload.

## API Endpoints

### 1. Unified Analysis Endpoint

**URL**: `POST /api/companies/{company_id}/analyse`

#### General Analysis Request
```bash
curl -X POST "http://localhost:5001/api/companies/company_123/analyse" \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Dynamic Risk Analysis Request
```bash
curl -X POST "http://localhost:5001/api/companies/company_123/analyse" \
  -H "Content-Type: application/json" \
  -d '{
    "risk_description": "New GDPR regulations require immediate data processing changes",
    "risk_context": "Additional context about the risk scenario",
    "risk_type": "regulatory"
  }'
```

### 2. Data Preparation Endpoint

**URL**: `POST /api/companies/{company_id}/send-to-ai`

This endpoint prepares comprehensive company data for external AI analysis.

```bash
curl -X POST "http://localhost:5001/api/companies/company_123/send-to-ai" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_endpoint_url": "https://your-ai-service.com/analyze"
  }'
```

## Data Structures

### Request Payload for Dynamic Risk Analysis

```json
{
  "risk_description": "New GDPR regulations require immediate data processing changes",
  "risk_context": "The company processes EU customer data and may be affected by new regulations",
  "risk_type": "regulatory"
}
```

### Internal Analysis Payload Structure

The system uses this internal structure when processing analysis requests:

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

### Complete Data Structure (send-to-ai endpoint)

Your AI service will receive this comprehensive payload:

```json
{
  "company_info": {
    "id": "company_123",
    "name": "Tesla Inc",
    "industry": "Automotive",
    "context": "Electric vehicle manufacturer",
    "documents": [
      {
        "file_name": "master_service_agreement.pdf",
        "file_type": "pdf",
        "content": "This Master Service Agreement (MSA) is entered into as of January 15, 2024...",
        "upload_date": "2024-01-15T10:00:00Z",
        "file_size": 2048576
      }
    ],
    "document_summary": {
      "total_documents": 4,
      "total_content_length": 51200,
      "document_types": ["pdf", "eml"]
    }
  },
  "news_data": {
    "total_results": 20,
    "search_metadata": {
      "api_version": "v1",
      "timestamp": "2024-01-15T12:00:00Z",
      "status": "success"
    },
    "articles_summary": [
      {
        "title": "Oil prices surge as Iran tensions escalate in Middle East",
        "description": "Global oil markets react to rising tensions between Iran and Western powers...",
        "content": "Oil prices surged to their highest level in months as tensions between Iran and Western powers escalated...",
        "url": "https://www.reuters.com/business/energy/oil-prices-surge-iran-tensions-escalate-2024-01-15/",
        "source": "Reuters",
        "published_date": "2024-01-15T10:00:00Z",
        "sentiment": "negative"
      }
    ]
  },
  "analysis_request": {
    "timestamp": "2024-01-15T12:00:00Z",
    "analysis_scope": [
      "regulatory_compliance",
      "operational_risks",
      "financial_exposure",
      "reputation_management",
      "legal_liabilities"
    ]
  }
}
```

## Expected Response Formats

### General Analysis Response

```json
{
  "risk_factors": [
    {
      "severity": "Low",
      "risk_type": "Reputational Risk",
      "affected_contracts": "contract.pdf",
      "affected_clauses": "Clause 1.1",
      "narrative": {
        "solutions_in_contract": "The contract does have a clause that addresses this risk. 16.1",
        "alternative_mitigations": "Do xyz to mitigate the risk.",
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

### Dynamic Risk Analysis Response

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
  "company_specific_insights": {
    "relevant_contracts": 3,
    "context_alignment": "High",
    "data_coverage": "Comprehensive",
    "critical_contracts_identified": "Multiple customer contracts with data processing clauses",
    "force_majeure_analysis": "Regulatory changes may trigger force majeure provisions"
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

## Integration Examples

### Python Integration

```python
import requests
import json
from typing import Optional, Dict, Any

class BusinessRiskAPI:
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url.rstrip('/')
    
    def analyze_company_general(self, company_id: str) -> Dict[str, Any]:
        """Perform general company risk analysis"""
        url = f"{self.base_url}/api/companies/{company_id}/analyse"
        
        response = requests.post(
            url,
            json={},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to analyze company: {response.text}")
    
    def analyze_dynamic_risk(
        self, 
        company_id: str, 
        risk_description: str, 
        risk_context: str = "", 
        risk_type: str = "unknown"
    ) -> Dict[str, Any]:
        """Perform dynamic risk analysis for a specific scenario"""
        url = f"{self.base_url}/api/companies/{company_id}/analyse"
        
        payload = {
            "risk_description": risk_description,
            "risk_context": risk_context,
            "risk_type": risk_type
        }
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to analyze dynamic risk: {response.text}")
    
    def prepare_data_for_ai(
        self, 
        company_id: str, 
        ai_endpoint_url: str
    ) -> Dict[str, Any]:
        """Prepare comprehensive company data for external AI analysis"""
        url = f"{self.base_url}/api/companies/{company_id}/send-to-ai"
        
        payload = {"ai_endpoint_url": ai_endpoint_url}
        
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to prepare data: {response.text}")

# Example usage
if __name__ == "__main__":
    api = BusinessRiskAPI()
    company_id = "company_123"
    
    try:
        # General analysis
        general_result = api.analyze_company_general(company_id)
        print("General Analysis:", json.dumps(general_result, indent=2))
        
        # Dynamic risk analysis
        dynamic_result = api.analyze_dynamic_risk(
            company_id,
            "New GDPR regulations require immediate data processing changes",
            "The company processes EU customer data and may be affected by new regulations",
            "regulatory"
        )
        print("Dynamic Risk Analysis:", json.dumps(dynamic_result, indent=2))
        
        # Prepare data for external AI
        ai_data = api.prepare_data_for_ai(
            company_id,
            "https://your-ai-service.com/analyze"
        )
        print("AI Data Prepared:", json.dumps(ai_data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
```

### JavaScript/Node.js Integration

```javascript
class BusinessRiskAPI {
    constructor(baseUrl = 'http://localhost:5001') {
        this.baseUrl = baseUrl.replace(/\/$/, '');
    }
    
    async analyzeCompanyGeneral(companyId) {
        const response = await fetch(`${this.baseUrl}/api/companies/${companyId}/analyse`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });
        
        if (!response.ok) {
            throw new Error(`Failed to analyze company: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    async analyzeDynamicRisk(companyId, riskDescription, riskContext = '', riskType = 'unknown') {
        const payload = {
            risk_description: riskDescription,
            risk_context: riskContext,
            risk_type: riskType
        };
        
        const response = await fetch(`${this.baseUrl}/api/companies/${companyId}/analyse`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });
        
        if (!response.ok) {
            throw new Error(`Failed to analyze dynamic risk: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    async prepareDataForAI(companyId, aiEndpointUrl) {
        const response = await fetch(`${this.baseUrl}/api/companies/${companyId}/send-to-ai`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ai_endpoint_url: aiEndpointUrl })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to prepare data: ${response.statusText}`);
        }
        
        return response.json();
    }
}

// Example usage
async function main() {
    const api = new BusinessRiskAPI();
    const companyId = 'company_123';
    
    try {
        // General analysis
        const generalResult = await api.analyzeCompanyGeneral(companyId);
        console.log('General Analysis:', JSON.stringify(generalResult, null, 2));
        
        // Dynamic risk analysis
        const dynamicResult = await api.analyzeDynamicRisk(
            companyId,
            'New GDPR regulations require immediate data processing changes',
            'The company processes EU customer data and may be affected by new regulations',
            'regulatory'
        );
        console.log('Dynamic Risk Analysis:', JSON.stringify(dynamicResult, null, 2));
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
```

## Analysis Guidelines

### Document Analysis
- **Extract key clauses** from legal documents
- **Identify risk triggers** and liability exposures
- **Assess compliance gaps** against industry standards
- **Evaluate contractual obligations** and penalties

### News Analysis
- **Analyze sentiment trends** across articles
- **Identify emerging risks** from current events
- **Assess market impact** on company operations
- **Connect news events** to company-specific risks

### Risk Scoring
- **Quantify risk levels** (Low, Medium, High, Critical)
- **Prioritize risks** by impact and probability
- **Provide confidence scores** for analysis
- **Include uncertainty factors**

## Error Handling

Your AI service should handle these scenarios:

1. **Missing Data**: Gracefully handle missing documents or news articles
2. **Invalid Content**: Process documents with extraction errors
3. **API Failures**: Continue analysis with available data
4. **Large Payloads**: Handle large document collections efficiently

## Performance Requirements

- **Response Time**: Target <30 seconds for analysis
- **Payload Size**: Handle up to 50MB of document content
- **Scalability**: Support concurrent analysis requests
- **Reliability**: 99.9% uptime for analysis service

## Security Considerations

- **Data Privacy**: Ensure secure handling of company information
- **Document Security**: Protect sensitive legal documents
- **API Security**: Use secure communication protocols
- **Data Retention**: Follow data retention policies

## Testing

Test your AI service with:

1. **Sample Company**: Use the provided example data
2. **Edge Cases**: Empty documents, missing news, large payloads
3. **Error Scenarios**: Invalid data, API failures
4. **Performance**: Large document collections

## Support

For technical questions or integration issues:
- **Documentation**: This guide and API documentation
- **Testing**: Use the provided example endpoints
- **Development**: Start with mock data for testing

---

**Note**: This integration enables comprehensive business risk analysis by combining company-specific data, legal documents, and real-time news to provide actionable risk insights. 