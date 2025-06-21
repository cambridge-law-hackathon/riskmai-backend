from flask import Blueprint, request, jsonify
from services import firebase_service
from services.news_service import NewsAPIService
from datetime import datetime
import requests
import os
from gradio_client import Client
import json

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/companies/<company_id>/analyse', methods=['POST'])
def analyse_company(company_id):
    """
    Unified analysis endpoint that sends data to AI service and stores results.
    
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
    
    # Fetch relevant news articles
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
                } for article in news_data.get("articles", [])[:3]  # Top 10 articles
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
    
    # Add risk scenario data if this is a dynamic risk analysis
    if is_dynamic_risk:
        analysis_payload["risk_scenario"] = {
            "description": data.get('risk_description'),
            "context": data.get('risk_context', ''),
            "type": data.get('risk_type', 'unknown'),
            "timestamp": datetime.now().isoformat()
        }

    analysis_payload = json.dumps(analysis_payload)

    client = Client("Baon2024/hackathon")
    result = client.predict(
		articles=analysis_payload,
		api_name="/predict"
    )
    print(result)
    
    # test_payload = {
    #     "analysis_id": "1",
    #     "risk_analysis": {
    #         "scenario": "Test risk scenario",
    #         "risk_level": "Medium", 
    #         "impact_assessment": "This is a test impact assessment",
    #         "affected_areas": ["Test Area 1", "Test Area 2"]
    #     },
    #     "recommendations": [
    #         "Test recommendation 1",
    #         "Test recommendation 2"
    #     ],
    #     "next_steps": [
    #         "Test next step 1",
    #         "Test next step 2"  
    #     ],
    #     "ai_confidence": 0.95,
    #     "analysis_timestamp": datetime.now().isoformat()
    # }

    
    # Store analysis results in database
    analysis_id, error = firebase_service.store_analysis_result(
        company_id=company_id,
        analysis_type="dynamic_risk" if is_dynamic_risk else "general",
        payload=analysis_payload,
        result=result,
        timestamp=datetime.now().isoformat()
    )
    
    if error:
        return jsonify({"error": f"Failed to store analysis: {error}"}), 500
    
    # Convert result to dict if it's a string
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse AI service response"}), 500
    
    # Add analysis ID to response
    result["analysis_id"] = analysis_id
    
    return jsonify(result), 200


@analysis_bp.route('/companies/<company_id>/analyses', methods=['GET'])
def get_company_analyses(company_id):
    """
    Get all analysis results for a company.
    
    Query parameters:
    - analysis_id: Get specific analysis by ID
    - analysis_type: Filter by analysis type ("general" or "dynamic_risk")
    - limit: Limit number of results (default: 10)
    """
    # Check if company exists
    company_data, error = firebase_service.get_company_data(company_id)
    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404
    
    # Get query parameters
    analysis_id = request.args.get('analysis_id')
    analysis_type = request.args.get('analysis_type')
    limit = int(request.args.get('limit', 10))
    
    # Get analyses from database
    analyses, error = firebase_service.get_company_analyses(
        company_id=company_id,
        analysis_id=analysis_id,
        analysis_type=analysis_type,
        limit=limit
    )
    
    if error:
        return jsonify({"error": error}), 500
    
    return jsonify(analyses), 200


@analysis_bp.route('/companies/<company_id>/analyses/<analysis_id>', methods=['GET'])
def get_analysis_by_id(company_id, analysis_id):
    """
    Get a specific analysis result by ID.
    """
    # Check if company exists
    company_data, error = firebase_service.get_company_data(company_id)
    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404
    
    # Get specific analysis
    analysis, error = firebase_service.get_analysis_by_id(company_id, analysis_id)
    
    if error:
        return jsonify({"error": error}), 500
    
    if not analysis:
        return jsonify({"error": "Analysis not found"}), 404
    
    return jsonify(analysis), 200 
