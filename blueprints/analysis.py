from flask import Blueprint, request, jsonify
from services import firebase_service
from services.news_service import NewsAPIService
from datetime import datetime

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/companies/<company_id>/analyse', methods=['POST'])
def analyse_company(company_id):
    # For now, this is a placeholder for the black box AI agent.
    # We will fetch company data and simulate an analysis.

    company_data, error = firebase_service.get_company_data(company_id)

    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404

    # Extract relevant data for analysis
    company_name = company_data.get('name', 'Unknown Company')
    context_items = company_data.get('context', [])
    documents = company_data.get('documents', [])
    
    # Count documents and their content
    total_documents = len(documents)
    total_content_length = sum(len(doc.get('content', '')) for doc in documents)
    
    # Fetch relevant news articles
    try:
        news_service = NewsAPIService()
        news_data = news_service.get_company_specific_news(company_name, days_back=30)
    except Exception as e:
        print(f"Error fetching news: {e}")
        news_data = {"articles": [], "total_results": 0, "error": str(e)}
    
    # Create a summary of available data
    data_summary = {
        "company_name": company_name,
        "context_items_count": len(context_items),
        "documents_count": total_documents,
        "total_content_length": total_content_length,
        "context_items": context_items,
        "document_names": [doc.get('file_name', 'Unknown') for doc in documents],
        "news_articles_count": news_data.get("total_results", 0)
    }

    # Here you would typically call the news searching AI agent
    # with company_data and news_data to get real analysis.
    
    # For now, provide a realistic analysis based on available data
    analysis_result = {
        "company_info": data_summary,
        "news_context": {
            "articles_found": news_data.get("total_results", 0),
            "recent_news": news_data.get("articles", [])[:5],  # Top 5 articles
            "search_query": news_data.get("query", "")
        },
        "analysis_summary": f"Analysis completed for {company_name}. Found {len(context_items)} context items, {total_documents} documents, and {news_data.get('total_results', 0)} relevant news articles.",
        "risk_factors": [
            {
                "factor": "Data Completeness", 
                "level": "Medium" if total_documents > 0 else "High", 
                "details": f"Company has {total_documents} documents and {len(context_items)} context items for analysis."
            },
            {
                "factor": "News Coverage", 
                "level": "Low" if news_data.get("total_results", 0) > 5 else "Medium", 
                "details": f"Found {news_data.get('total_results', 0)} relevant news articles in the past 30 days."
            },
            {
                "factor": "Content Volume", 
                "level": "Low" if total_content_length > 10000 else "Medium", 
                "details": f"Total content available: {total_content_length} characters."
            }
        ],
        "recommendations": [
            "Consider adding more context about the company's operations and risk profile.",
            "Upload additional legal documents for comprehensive analysis.",
            "Monitor news coverage for emerging risks and regulatory changes."
        ],
        "available_data": {
            "context_items": context_items,
            "document_count": total_documents,
            "content_available": total_content_length > 0,
            "news_available": news_data.get("total_results", 0) > 0
        }
    }

    return jsonify(analysis_result), 200

@analysis_bp.route('/companies/<company_id>/dynamic-risk', methods=['POST'])
def analyze_dynamic_risk(company_id):
    """
    Analyze a specific dynamic risk scenario for a company.
    Combines user-provided risk information with company context, documents, and relevant news.
    """
    data = request.get_json()
    if not data or not 'risk_description' in data:
        return jsonify({"error": "Risk description is required"}), 400
    
    risk_description = data.get('risk_description')
    risk_context = data.get('risk_context', '')  # Additional context about the risk
    risk_type = data.get('risk_type', 'unknown')  # e.g., 'regulatory', 'operational', 'financial'
    
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
    
    # Fetch relevant news articles for the specific risk scenario
    try:
        news_service = NewsAPIService()
        news_data = news_service.get_risk_specific_news(
            risk_description=risk_description,
            risk_type=risk_type,
            company_name=company_name
        )
    except Exception as e:
        print(f"Error fetching news: {e}")
        news_data = {"articles": [], "total_results": 0, "error": str(e)}
    
    # Prepare data for AI agent
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
        "risk_scenario": {
            "description": risk_description,
            "context": risk_context,
            "type": risk_type,
            "timestamp": datetime.now().isoformat()
        },
        "news_context": {
            "articles": news_data.get("articles", []),
            "total_results": news_data.get("total_results", 0),
            "search_query": news_data.get("query", ""),
            "recent_developments": [
                {
                    "title": article.get("title"),
                    "summary": article.get("description"),
                    "source": article.get("source"),
                    "date": article.get("published_date"),
                    "sentiment": article.get("sentiment")
                } for article in news_data.get("articles", [])[:10]  # Top 10 articles
            ]
        }
    }
    
    # Here you would call the AI agent with the analysis_payload
    # For now, provide a simulated analysis
    ai_analysis = simulate_ai_analysis(analysis_payload)
    
    return jsonify(ai_analysis), 200

def simulate_ai_analysis(payload):
    """
    Simulate AI agent analysis of dynamic risk scenario.
    In production, this would call your actual AI agent.
    """
    company_name = payload["company_info"]["name"]
    risk_description = payload["risk_scenario"]["description"]
    risk_type = payload["risk_scenario"]["type"]
    news_articles = payload.get("news_context", {}).get("articles", [])
    
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
