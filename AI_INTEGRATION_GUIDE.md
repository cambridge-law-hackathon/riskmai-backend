# AI Integration Guide for Business Risk Analysis

## Overview

This guide explains the data structure and format that your AI service will receive when analyzing business risks for companies. The system provides comprehensive company information, legal documents, and relevant news articles to enable thorough risk assessment.

## API Endpoint

**URL:** `POST /companies/{company_id}/send-to-ai`

**Base URL:** `http://localhost:5000` (or your deployed server URL)

## Request Format

```bash
curl -X POST "http://localhost:5000/companies/company_123/send-to-ai" \
  -H "Content-Type: application/json" \
  -d '{
    "ai_endpoint_url": "https://your-ai-service.com/analyze-risk"
  }'
```

## Complete Data Structure You Will Receive

Your AI service will receive this complete JSON payload:

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
        "content": "This Master Service Agreement (MSA) is entered into as of January 15, 2024, between Tesla Inc, a Delaware corporation with its principal place of business at 1 Tesla Road, Austin, TX 78725 (\"Customer\") and CloudTech Solutions Inc, a California corporation (\"Provider\").\n\n1. SERVICES\nProvider shall provide cloud infrastructure services including compute, storage, and networking resources as specified in each Statement of Work (SOW).\n\n2. SERVICE LEVEL AGREEMENTS\nProvider guarantees 99.9% uptime for all services. For each hour of downtime below 99.9%, Customer shall receive a credit equal to 300% of the monthly fee for affected services.\n\n3. FORCE MAJEURE\nNeither party shall be liable for any delay or failure to perform due to circumstances beyond its reasonable control, including but not limited to acts of God, war, terrorism, riots, fire, natural disasters, government actions, or labor disputes.\n\n4. TERMINATION\nEither party may terminate this agreement with 30 days written notice. Upon termination, Provider shall assist Customer in migrating data and services to an alternative provider.\n\n5. LIABILITY\nProvider's total liability shall not exceed the amount paid by Customer in the 12 months preceding the claim. Neither party shall be liable for indirect, incidental, or consequential damages.",
        "upload_date": "2024-01-15T10:00:00Z",
        "file_size": 2048576
      },
      {
        "file_name": "compliance_report_2024.pdf",
        "file_type": "pdf",
        "content": "Tesla Inc - Annual Compliance Report 2024\n\nRegulatory Compliance Summary:\n- Automotive Safety Standards: Fully compliant with NHTSA requirements\n- Environmental Regulations: Meets EPA emissions standards for manufacturing\n- Data Protection: GDPR and CCPA compliant for customer data handling\n- Financial Reporting: SEC compliance maintained\n- International Trade: All export controls and sanctions requirements met\n\nRisk Assessment:\n- Supply chain disruptions: Medium risk due to semiconductor shortages\n- Regulatory changes: High risk in autonomous driving regulations\n- Cybersecurity: Medium risk with increasing threat landscape\n- Geopolitical: High risk due to US-China trade tensions\n\nRecommendations:\n- Diversify semiconductor suppliers\n- Monitor autonomous driving regulatory developments\n- Enhance cybersecurity protocols\n- Develop contingency plans for trade restrictions",
        "upload_date": "2024-01-14T15:30:00Z",
        "file_size": 1536000
      },
      {
        "file_name": "insurance_policy.pdf",
        "file_type": "pdf",
        "content": "Commercial General Liability Insurance Policy\n\nInsured: Tesla Inc\nPolicy Period: January 1, 2024 - January 1, 2025\n\nCoverage Limits:\n- General Aggregate: $10,000,000\n- Products Liability: $5,000,000\n- Personal and Advertising Injury: $1,000,000\n- Medical Payments: $10,000 per person\n\nExclusions:\n- Intentional acts\n- Pollution liability\n- Professional liability\n- Cyber liability (separate policy required)\n\nDeductible: $50,000 per occurrence\n\nAdditional Insured: CloudTech Solutions Inc (as required by MSA)",
        "upload_date": "2024-01-13T09:15:00Z",
        "file_size": 1024000
      },
      {
        "file_name": "legal_correspondence.eml",
        "file_type": "eml",
        "content": "From: legal@tesla.com\nTo: contracts@cloudtech.com\nSubject: Force Majeure Notice - Service Agreement\nDate: January 10, 2024\n\nDear CloudTech Solutions,\n\nWe are writing to formally dispute your force majeure declaration dated January 8, 2024, regarding the 300% cost increase across all cloud services.\n\nTesla Inc believes that the circumstances you have cited do not meet the legal definition of force majeure under our Master Service Agreement. The geopolitical tensions and supply chain disruptions you reference are foreseeable business risks that do not constitute unforeseeable events beyond your reasonable control.\n\nFurthermore, the magnitude of the proposed cost increase (300%) appears to be disproportionate to any actual cost increases you may be experiencing. We request detailed documentation supporting your cost increase claims.\n\nTesla Inc reserves all rights under the agreement and will vigorously defend our position. We are prepared to engage in good faith negotiations to reach a mutually acceptable resolution.\n\nPlease respond within 5 business days with your proposed path forward.\n\nBest regards,\nTesla Legal Team",
        "upload_date": "2024-01-10T14:20:00Z",
        "file_size": 512000
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
        "description": "Global oil markets react to rising tensions between Iran and Western powers, with Brent crude reaching $95 per barrel as supply concerns mount.",
        "content": "Oil prices surged to their highest level in months as tensions between Iran and Western powers escalated, raising concerns about potential supply disruptions in the critical Strait of Hormuz. Brent crude futures rose 4.2% to $95.23 per barrel, while West Texas Intermediate climbed 3.8% to $91.45.\n\nThe price spike comes amid reports that Iran has increased its nuclear enrichment activities and continues to support proxy groups in the region. Analysts warn that any military conflict could severely disrupt oil shipments through the Persian Gulf, which handles about 20% of global oil trade.\n\n'This is exactly the kind of geopolitical risk that keeps energy markets on edge,' said Sarah Chen, senior energy analyst at Global Markets Research. 'The combination of supply constraints and geopolitical tensions creates a perfect storm for price volatility.'\n\nManufacturing companies, particularly in the automotive sector, are already feeling the impact of higher energy costs. Tesla Inc and other electric vehicle manufacturers may face increased production costs despite their focus on sustainable energy, as their supply chains remain dependent on traditional energy sources for manufacturing and logistics.\n\nThe situation has prompted calls for accelerated investment in renewable energy and energy independence initiatives. However, experts note that the transition will take years, leaving companies vulnerable to energy price shocks in the meantime.",
        "url": "https://www.reuters.com/business/energy/oil-prices-surge-iran-tensions-escalate-2024-01-15/",
        "source": "Reuters",
        "published_date": "2024-01-15T10:00:00Z",
        "sentiment": "negative"
      },
      {
        "title": "Natural gas supply disruptions impact global manufacturing sector",
        "description": "Manufacturing costs rise as natural gas prices increase by 25% due to supply chain disruptions and geopolitical tensions affecting energy markets.",
        "content": "Global manufacturing companies are facing significant cost increases as natural gas prices have surged 25% over the past month, driven by supply chain disruptions and geopolitical tensions in key energy-producing regions.\n\nThe price increase is particularly affecting energy-intensive industries such as automotive manufacturing, where companies like Tesla Inc rely on natural gas for various production processes including aluminum smelting, glass manufacturing, and facility heating.\n\n'Energy costs represent a significant portion of our manufacturing expenses,' said a spokesperson for Tesla Inc. 'While we're committed to sustainable energy solutions, our current manufacturing processes still require traditional energy sources, and these price increases directly impact our cost structure.'\n\nAnalysts estimate that the energy price increases could add $500-800 to the production cost of each electric vehicle, potentially affecting profit margins and pricing strategies across the industry.\n\nThe situation has prompted renewed calls for investment in renewable energy infrastructure and energy storage solutions. However, industry experts note that the transition to fully renewable manufacturing processes will require significant capital investment and time.\n\n'Companies need to balance immediate cost pressures with long-term sustainability goals,' said Michael Rodriguez, manufacturing analyst at Industry Insights. 'The current energy price volatility underscores the importance of diversifying energy sources and investing in energy efficiency.'",
        "url": "https://www.bloomberg.com/news/articles/2024-01-14/natural-gas-disruptions-impact-manufacturing",
        "source": "Bloomberg",
        "published_date": "2024-01-14T15:30:00Z",
        "sentiment": "neutral"
      },
      {
        "title": "Iran sanctions enforcement tightened by US Treasury Department",
        "description": "The US Treasury Department announces enhanced enforcement of Iran sanctions, affecting global supply chains and energy markets.",
        "content": "The US Treasury Department has announced enhanced enforcement measures for Iran-related sanctions, including stricter monitoring of supply chains and financial transactions. The new measures target companies that may be indirectly supporting Iran's energy sector or nuclear program.\n\nThe enhanced enforcement includes:\n- Increased scrutiny of third-party transactions\n- Expanded secondary sanctions targeting non-US companies\n- Stricter requirements for supply chain due diligence\n- Enhanced penalties for violations\n\n'These measures are designed to prevent Iran from circumventing sanctions through complex supply chain arrangements,' said Treasury Secretary Janet Yellen. 'Companies must ensure they are not inadvertently supporting sanctioned entities.'\n\nThe announcement has caused concern among global manufacturers who source materials or components from regions that may have indirect connections to Iran. Automotive manufacturers, including Tesla Inc, are particularly vulnerable as they rely on global supply chains for critical components.\n\nLegal experts advise companies to conduct thorough supply chain audits and implement enhanced due diligence procedures. 'The penalties for sanctions violations can be severe,' said legal counsel Jennifer Martinez. 'Companies need to understand their entire supply chain and ensure compliance.'\n\nThe enhanced enforcement comes amid rising tensions between Iran and Western powers, with implications for global energy markets and manufacturing costs.",
        "url": "https://www.wsj.com/articles/iran-sanctions-enforcement-tightened-2024-01-13/",
        "source": "Wall Street Journal",
        "published_date": "2024-01-13T09:15:00Z",
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

## Expected AI Analysis Output

Your AI service should return a comprehensive risk analysis in this format:

```json
{
  "risk_analysis": {
    "overall_risk_level": "Critical",
    "risk_score": 0.92,
    "key_risk_factors": [
      {
        "factor": "Cloud Infrastructure Force Majeure",
        "level": "Critical",
        "description": "Provider has declared force majeure and demanded 300% cost increases",
        "impact": "$2.3 billion in annual recurring revenue at risk"
      },
      {
        "factor": "Energy Price Volatility",
        "level": "High",
        "description": "Oil and gas prices surging due to Iran tensions",
        "impact": "Increased manufacturing costs and supply chain disruption"
      },
      {
        "factor": "Regulatory Compliance",
        "level": "Medium",
        "description": "Enhanced Iran sanctions enforcement",
        "impact": "Supply chain audit requirements and compliance costs"
      }
    ],
    "affected_business_areas": [
      "Operations",
      "Finance", 
      "Legal",
      "Reputation",
      "Supply Chain"
    ]
  },
  "news_analysis": {
    "relevant_articles_count": 20,
    "sentiment_trend": "negative",
    "key_trends": [
      "Rising energy costs affecting manufacturing",
      "Iran sanctions enforcement tightening",
      "Cloud infrastructure price increases",
      "Supply chain disruptions"
    ],
    "market_impact": "Energy price increases could add $500-800 to EV production costs"
  },
  "document_analysis": {
    "contract_risks": [
      "Force majeure clause may not cover energy price increases",
      "300% liquidated damages for SLA violations",
      "30-day termination notice requirement",
      "Limited liability caps may not cover full damages"
    ],
    "compliance_gaps": [
      "Supply chain due diligence for Iran sanctions",
      "Energy efficiency requirements",
      "Cybersecurity insurance coverage"
    ],
    "legal_exposure": "High exposure to contractual disputes and regulatory penalties"
  },
  "recommendations": [
    {
      "priority": "Critical",
      "category": "Legal",
      "action": "Challenge force majeure declaration and negotiate cost increases",
      "timeline": "Immediate",
      "impact": "Prevent 300% cost increase and service termination"
    },
    {
      "priority": "High",
      "category": "Operations",
      "action": "Implement energy efficiency measures and diversify energy sources",
      "timeline": "30 days",
      "impact": "Reduce energy cost exposure by 15-20%"
    },
    {
      "priority": "High",
      "category": "Compliance",
      "action": "Conduct supply chain audit for Iran sanctions compliance",
      "timeline": "60 days",
      "impact": "Avoid regulatory penalties and maintain market access"
    }
  ],
  "next_steps": [
    "Immediate legal response to force majeure claim",
    "Energy cost mitigation strategy development",
    "Supply chain compliance audit",
    "Alternative cloud provider evaluation"
  ],
  "ai_confidence": 0.92,
  "analysis_timestamp": "2024-01-15T12:00:00Z"
}
```

## Processing Guidelines

### 1. Document Analysis
- **Extract key clauses** from legal documents
- **Identify risk triggers** and liability exposures
- **Assess compliance gaps** against industry standards
- **Evaluate contractual obligations** and penalties

### 2. News Analysis
- **Analyze sentiment trends** across articles
- **Identify emerging risks** from current events
- **Assess market impact** on company operations
- **Connect news events** to company-specific risks

### 3. Context Integration
- **Combine company context** with document analysis
- **Cross-reference news** with company operations
- **Industry-specific risk assessment**
- **Geographic and regulatory considerations**

### 4. Risk Scoring
- **Quantify risk levels** (0-1 scale)
- **Prioritize risks** by impact and probability
- **Provide confidence scores** for analysis
- **Include uncertainty factors**

## Error Handling

Your AI service should handle these scenarios:

1. **Missing Data**: Gracefully handle missing documents or news articles
2. **Invalid Content**: Process documents with extraction errors
3. **API Failures**: Continue analysis with available data
4. **Large Payloads**: Handle large document collections efficiently

## Security Considerations

- **Data Privacy**: Ensure secure handling of company information
- **Document Security**: Protect sensitive legal documents
- **API Security**: Use secure communication protocols
- **Data Retention**: Follow data retention policies

## Performance Requirements

- **Response Time**: Target <30 seconds for analysis
- **Payload Size**: Handle up to 50MB of document content
- **Scalability**: Support concurrent analysis requests
- **Reliability**: 99.9% uptime for analysis service

## Testing

Test your AI service with:

1. **Sample Company**: Use the provided example data
2. **Edge Cases**: Empty documents, missing news, large payloads
3. **Error Scenarios**: Invalid data, API failures
4. **Performance**: Large document collections

## Integration Example

```python
import requests
import json

def analyze_company_risk(company_id, ai_endpoint_url):
    # Get prepared data from business risk platform
    response = requests.post(
        f"http://localhost:5000/companies/{company_id}/send-to-ai",
        json={"ai_endpoint_url": ai_endpoint_url}
    )
    
    if response.status_code == 200:
        data = response.json()
        ai_payload = data["ai_payload"]
        
        # Send to your AI service
        ai_response = requests.post(
            ai_endpoint_url,
            json=ai_payload,
            headers={"Content-Type": "application/json"}
        )
        
        return ai_response.json()
    else:
        raise Exception(f"Failed to prepare data: {response.text}")
```

## Support

For technical questions or integration issues:
- **Documentation**: This guide and API documentation
- **Testing**: Use the provided example endpoints
- **Development**: Start with mock data for testing

---

**Note**: This integration enables comprehensive business risk analysis by combining company-specific data, legal documents, and real-time news to provide actionable risk insights. 