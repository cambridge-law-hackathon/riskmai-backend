from flask import Blueprint, request, jsonify
from services import firebase_service
from services.news_service import NewsAPIService
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/companies/<company_id>/analyse', methods=['POST'])
def analyse_company(company_id):
    """
    Unified analysis endpoint that handles both general company analysis and dynamic risk analysis.
    
    For general analysis: Send empty body or {}
    For dynamic risk analysis: Send {"risk_description": "...", "risk_context": "...", "risk_type": "..."}
    """
    data = request.get_json() or {}
    
    # Check if this is a dynamic risk analysis request
    is_dynamic_risk = 'risk_description' in data
    
    # Get company data including context and documents
    company_data, error = firebase_service.get_company_data(company_id)
    
    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404

    # Extract company information
    company_name = company_data.get('name', 'Unknown Company')
    company_context = company_data.get('context', [])
    documents = company_data.get('documents', [])
    
    # Fetch relevant news articles based on analysis type
    try:
        news_service = NewsAPIService()
        news_data = news_service.get_company_specific_news(company_name, days_back=30)
    except Exception as e:
        print(f"Error fetching news: {e}")
        news_data = {"articles": [], "total_results": 0, "error": str(e)}
    
    # Prepare analysis payload
    analysis_payload = {
        "company_info": {
            "name": company_name,
            "context": company_context,
            "documents": [
                {
                    "file_name": doc.get('file_name'),
                    "content": doc.get('content'),
                    "file_type": doc.get('file_type')
                } for doc in documents
            ]
        },
        "news_data": {
            "articles_summary": [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "source": article.get("source"),
                    "date": article.get("published_date"),
                    "sentiment": article.get("sentiment")
                } for article in news_data.get("articles", [])[:10]  # Top 10 articles
            ]
        }
    }
    
    # Add risk scenario data if this is a dynamic risk analysis
    if is_dynamic_risk:
        analysis_payload["risk_scenario"] = {
            "description": data.get('risk_description'),
            "context": data.get('risk_context', ''),
            "type": data.get('risk_type', 'unknown'),
            "timestamp": datetime.now().isoformat()
        }
    
    # Generate appropriate analysis based on request type
    if is_dynamic_risk:
        analysis_result = simulate_dynamic_risk_analysis(analysis_payload)
    else:
        analysis_result = simulate_general_analysis(analysis_payload)
    
    return jsonify(analysis_result), 200


def simulate_general_analysis(payload):
    """
    Simulate AI agent analysis for general company risk assessment.
    """
    company_name = payload["company_info"]["name"]
    context_items = payload["company_info"]["context"]
    documents = payload["company_info"]["documents"]
    news_articles = payload.get("news_data", {}).get("articles_summary", [])
    
    # Count documents and their content
    total_documents = len(documents)
    total_content_length = sum(len(doc.get('content', '')) for doc in documents)
    
    # Analyze news sentiment
    relevant_news_count = len(news_articles)
    negative_sentiment_count = len([a for a in news_articles if a.get("sentiment") == "negative"])
    
    # Generate risk factors based on available data
    risk_factors = []
    risk_factors.append({
        "severity": "Low",
        "risk_type": "Reputational Risk",
        "affected_contracts": "contract.pdf",
        "affected_clauses": "Clause 1.1",
        "narrative":{
            "solutions_in_contract": "The contract does have a clause that addresses this risk. 16.1",
            "alternative_mitigations": "Do xyz to mitigate the risk.",
            "monitoring_tasks": "Monitor the risk and report to the board every 3 months.",

        }
    })
    return {
        "risk_factors": risk_factors,
        "available_data": {
            "context_items": context_items,
            "document_count": total_documents,
            "content_available": total_content_length > 0,
            "news_available": relevant_news_count > 0
        }
    }

def simulate_dynamic_risk_analysis(payload):
    """
    Simulate AI agent analysis of dynamic risk scenario.
    """
    company_name = payload["company_info"]["name"]
    risk_description = payload["risk_scenario"]["description"]
    risk_type = payload["risk_scenario"]["type"]
    news_articles = payload.get("news_data", {}).get("articles_summary", [])
    
    # Analyze news sentiment and relevance
    relevant_news_count = len(news_articles)
    negative_sentiment_count = len([a for a in news_articles if a.get("sentiment") == "negative"])
    
    # Simulate AI processing
    analysis_result = {
        "risk_analysis": {
            "scenario": risk_description,
            "risk_level": "Critical" if any(word in risk_description.lower() for word in ["force majeure", "breach", "liquidated damages", "300%"]) else "High",
            "impact_assessment": f"This {risk_type} risk represents an existential threat to {company_name}'s business operations, with $2.3 billion in annual recurring revenue at immediate risk. The combination of potential service interruptions, massive cost increases, and contractual breach scenarios creates a perfect storm of legal and operational challenges that require immediate executive attention and coordinated legal response.",
            "affected_areas": [
                "Contractual obligations and SLA compliance",
                "Customer relationship management and retention",
                "Financial stability and cash flow",
                "Operational continuity and disaster recovery",
                "Regulatory compliance and reporting"
            ]
        },
        "news_analysis": {
            "articles_found": relevant_news_count,
            "negative_sentiment_ratio": negative_sentiment_count / max(relevant_news_count, 1),
            "trending_topics": [article.get("title") for article in news_articles[:3]],
            "market_context": f"Found {relevant_news_count} relevant articles with {negative_sentiment_count} showing negative sentiment"
        },
        "company_specific_insights": {
            "relevant_contracts": len([doc for doc in payload["company_info"]["documents"] if doc.get("file_type") == "pdf"]),
            "context_alignment": "High" if payload["company_info"]["context"] else "Low",
            "data_coverage": "Comprehensive" if len(payload["company_info"]["documents"]) > 2 else "Limited",
            "critical_contracts_identified": "Multiple customer contracts with uptime SLAs and liquidated damages clauses",
            "force_majeure_analysis": "Provider's claim appears weak given industry-wide pattern"
        },
        "recommendations": [
            "Immediate Legal Response: Engage outside counsel specializing in cloud infrastructure disputes to challenge the force majeure claim, as the provider's position appears to be a coordinated industry-wide renegotiation tactic rather than genuine force majeure circumstances. Review all existing contracts for force majeure definitions, notice requirements, and alternative dispute resolution mechanisms. Prepare for potential litigation while simultaneously exploring settlement options that protect customer relationships and minimize financial exposure.",
            "Customer Communication Strategy: Develop a comprehensive communication plan to proactively address customer concerns about potential service disruptions. Consider offering contractual amendments that provide additional assurances or compensation for any service interruptions, while maintaining the legal right to pass through reasonable cost increases. Establish a dedicated customer success team to handle inquiries and maintain trust during the transition period.",
            "Infrastructure Migration Planning: Immediately initiate parallel infrastructure deployment with alternative cloud providers to create redundancy and reduce dependency on the current provider. Allocate the necessary $15 million budget and establish a cross-functional migration team with clear timelines and milestones. Negotiate with alternative providers for favorable terms given the urgent nature of the situation and the potential for long-term partnership."
        ],
        "next_steps": [
            "Executive Crisis Management: Convene an emergency board meeting within 24 hours to approve immediate legal budget allocation and establish executive oversight committee. Appoint a crisis management team with representatives from legal, operations, finance, and customer success. Establish daily executive briefings and weekly board updates to ensure coordinated response across all business functions.",
            "Financial Risk Mitigation: Immediately review all insurance policies for coverage related to business interruption, cyber liability, and professional liability that may apply to this situation. Assess current cash position and establish credit facilities to cover potential legal costs and infrastructure migration expenses. Develop financial contingency plans for worst-case scenarios including customer churn and revenue impact.",
            "Regulatory and Compliance Review: Conduct immediate review of all regulatory obligations that may be triggered by potential service interruptions, including data protection, financial services, and industry-specific compliance requirements. Prepare regulatory notifications and establish communication protocols with relevant authorities. Ensure all customer data protection and privacy obligations can be maintained during any transition period."
        ],
        "ai_confidence": 0.92,
        "analysis_timestamp": datetime.now().isoformat()
    }
    
    return analysis_result

@analysis_bp.route('/companies/<company_id>/send-to-ai', methods=['POST'])
def send_to_ai_endpoint(company_id):
    """
    Prepare company data and news articles, then send to external AI endpoint for analysis.
    """
    data = request.get_json() or {}
    ai_endpoint_url = data.get('ai_endpoint_url', 'https://your-ai-endpoint.com/analyze')
    
    # Get company data including context and documents
    company_data, error = firebase_service.get_company_data(company_id)
    
    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404

    # Extract company information
    company_name = company_data.get('name', 'Unknown Company')
    company_context = company_data.get('context', "No context provided")
    documents = company_data.get('documents', [])
    
    # Fetch relevant news articles
    try:
        news_service = NewsAPIService()
        news_data = news_service.search_news(
            query=None,
            company_name=company_name,
            days_back=30
        )
    except Exception as e:
        print(f"Error fetching news: {e}")
        news_data = {"articles": [], "total_results": 0, "error": str(e)}
    
    # Prepare the payload to send to AI endpoint
    ai_payload = {
        "company_info": {
            "id": company_id,
            "name": company_name,
            "industry": company_data.get('industry', 'Unknown'),
            "context": company_context,
            "documents": [
                {
                    "file_name": doc.get('file_name'),
                    "file_type": doc.get('file_type'),
                    "content": doc.get('content'),
                    "upload_date": doc.get('upload_date'),
                    "file_size": doc.get('file_size')
                } for doc in documents
            ],
            "document_summary": {
                "total_documents": len(documents),
                "total_content_length": sum(len(doc.get('content', '')) for doc in documents),
                "document_types": list(set(doc.get('file_type') for doc in documents))
            }
        },
        "news_data": {
            "total_results": news_data.get("total_results", 0),
            "search_metadata": news_data.get("search_metadata", {}),
            "articles_summary": [
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "content": article.get("content"),
                    "url": article.get("url"),
                    "source": article.get("source"),
                    "published_date": article.get("published_date"),
                    "sentiment": article.get("sentiment"),
                } for article in news_data.get("articles", [])
            ]
        },
        "analysis_request": {
            "timestamp": datetime.now().isoformat(),
            "analysis_scope": [
                "regulatory_compliance",
                "operational_risks", 
                "financial_exposure",
                "reputation_management",
                "legal_liabilities"
            ]
        }
    }
    
    # Here you would send the ai_payload to your external AI endpoint
    # For now, return the prepared payload
    return jsonify({
        "message": "Data prepared for AI analysis",
        "ai_endpoint_url": ai_endpoint_url,
        "payload_size": len(str(ai_payload)),
        "company_name": company_name,
        "documents_count": len(documents),
        "news_articles_count": len(news_data.get("articles", [])),
        "ai_payload": ai_payload
    }), 200 
