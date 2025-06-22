from flask import Blueprint, request, jsonify
from services import firebase_service
from services.news_service import NewsAPIService
from datetime import datetime
import requests
import os
from openai import OpenAI
import json

analysis_bp = Blueprint('analysis', __name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
        # Prepare the prompt for dynamic risk analysis
        dynamic_risk_prompt = f"""
You are a legal intelligence AI assistant helping General Counsels assess business risks. 

Company Information:
- Name: {company_name}
- Context: {company_context}
- Documents: {len(documents)} documents uploaded
- News Articles: {len(news_data.get('articles', []))} recent articles

Risk Scenario to Analyze:
{data.get('risk_description', '')}

Context: {data.get('risk_context', '')}
Risk Type: {data.get('risk_type', 'General')}

Recent News Articles:
{chr(10).join([f"- {article.get('title', 'No title')} ({article.get('source', 'Unknown source')} - {article.get('published_date', 'Unknown date')}): {article.get('description', 'No description')}" for article in news_data.get('articles', [])[:5]])}

Please provide a comprehensive risk analysis in the following JSON format:
{{
    "risk_analysis": {{
        "scenario": "Brief description of the risk scenario",
        "risk_level": "Low/Medium/High/Critical",
        "impact_assessment": "Detailed assessment of potential impacts",
        "affected_areas": ["Area 1", "Area 2", "Area 3"],
        "legal_implications": "Analysis of legal consequences",
        "regulatory_considerations": "Relevant regulatory issues",
        "news_triggers": [
            {{
                "article_title": "Title of the news article",
                "article_source": "Source of the article",
                "article_date": "Date of the article",
                "risk_connection": "How this article relates to the identified risk"
            }}
        ]
    }},
    "recommendations": [
        "Specific actionable recommendation 1",
        "Specific actionable recommendation 2",
        "Specific actionable recommendation 3"
    ],
    "next_steps": [
        "Immediate next step 1",
        "Immediate next step 2",
        "Immediate next step 3"
    ],
    "ai_confidence": 0.85,
    "analysis_timestamp": "{datetime.now().isoformat()}"
}}

Provide detailed, lawyer-style analysis with specific legal considerations and actionable recommendations. For each risk identified, reference the specific news articles that triggered or influenced that risk assessment.
"""

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a legal intelligence AI assistant specializing in business risk assessment for General Counsels. Always respond with valid JSON in the exact format requested."},
                    {"role": "user", "content": dynamic_risk_prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                final_result = json.loads(ai_response)
            except json.JSONDecodeError as e:
                print(f"JSON decode error for dynamic risk: {e}")
                print(f"Raw AI response was: {ai_response}")
                # If JSON parsing fails, create a structured response
                final_result = {
                    "risk_analysis": {
                        "scenario": data.get('risk_description', 'Unknown scenario'),
                        "risk_level": "Unknown",
                        "impact_assessment": ai_response,
                        "affected_areas": ["General"],
                        "legal_implications": "Analysis failed to parse properly",
                        "regulatory_considerations": "Analysis failed to parse properly",
                        "news_triggers": []
                    },
                    "recommendations": ["Review the raw analysis response"],
                    "next_steps": ["Contact technical support"],
                    "ai_confidence": 0.5,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            final_result = {
                "error": f"Failed to analyze risk: {str(e)}",
                "risk_analysis": {
                    "scenario": data.get('risk_description', 'Unknown scenario'),
                    "risk_level": "Unknown",
                    "impact_assessment": "Analysis failed due to API error",
                    "affected_areas": ["General"],
                    "legal_implications": "Analysis failed due to API error",
                    "regulatory_considerations": "Analysis failed due to API error",
                    "news_triggers": []
                },
                "recommendations": ["Check OpenAI API configuration"],
                "next_steps": ["Verify API key and network connection"],
                "ai_confidence": 0.0,
                "analysis_timestamp": datetime.now().isoformat()
            }

        # Store analysis results in database
        analysis_id, error = firebase_service.store_analysis_result(
            company_id=company_id,
            analysis_type="dynamic_risk",
            payload=analysis_payload,
            result=final_result,
            timestamp=datetime.now().isoformat()
        )
        
        if error:
            return jsonify({"error": f"Failed to store analysis: {error}"}), 500
        
        # Add analysis ID to response
        response_data = {"result": final_result, "analysis_id": analysis_id}
        
        return jsonify(response_data), 200

    else:
        # Prepare the prompt for general analysis
        general_analysis_prompt = f"""
You are a legal intelligence AI assistant helping General Counsels assess business risks. 

Company Information:
- Name: {company_name}
- Context: {company_context}
- Documents: {len(documents)} documents uploaded
- News Articles: {len(news_data.get('articles', []))} recent articles

Recent News Articles:
{chr(10).join([f"- {article.get('title', 'No title')} ({article.get('source', 'Unknown source')} - {article.get('published_date', 'Unknown date')}): {article.get('description', 'No description')}" for article in news_data.get('articles', [])[:5]])}

Please provide a comprehensive business risk analysis covering regulatory compliance, operational risks, financial exposure, reputation management, and legal liabilities.

Please provide the analysis in the following JSON format:
{{
    "risk_analysis": {{
        "regulatory_compliance": {{
            "risk_level": "Low/Medium/High/Critical",
            "assessment": "Detailed assessment of regulatory compliance risks",
            "key_concerns": ["Concern 1", "Concern 2", "Concern 3"],
            "news_triggers": [
                {{
                    "article_title": "Title of the news article",
                    "article_source": "Source of the article",
                    "article_date": "Date of the article",
                    "risk_connection": "How this article relates to regulatory compliance risks"
                }}
            ]
        }},
        "operational_risks": {{
            "risk_level": "Low/Medium/High/Critical",
            "assessment": "Detailed assessment of operational risks",
            "key_concerns": ["Concern 1", "Concern 2", "Concern 3"],
            "news_triggers": [
                {{
                    "article_title": "Title of the news article",
                    "article_source": "Source of the article",
                    "article_date": "Date of the article",
                    "risk_connection": "How this article relates to operational risks"
                }}
            ]
        }},
        "financial_exposure": {{
            "risk_level": "Low/Medium/High/Critical",
            "assessment": "Detailed assessment of financial exposure risks",
            "key_concerns": ["Concern 1", "Concern 2", "Concern 3"],
            "news_triggers": [
                {{
                    "article_title": "Title of the news article",
                    "article_source": "Source of the article",
                    "article_date": "Date of the article",
                    "risk_connection": "How this article relates to financial exposure risks"
                }}
            ]
        }},
        "reputation_management": {{
            "risk_level": "Low/Medium/High/Critical",
            "assessment": "Detailed assessment of reputation management risks",
            "key_concerns": ["Concern 1", "Concern 2", "Concern 3"],
            "news_triggers": [
                {{
                    "article_title": "Title of the news article",
                    "article_source": "Source of the article",
                    "article_date": "Date of the article",
                    "risk_connection": "How this article relates to reputation management risks"
                }}
            ]
        }},
        "legal_liabilities": {{
            "risk_level": "Low/Medium/High/Critical",
            "assessment": "Detailed assessment of legal liability risks",
            "key_concerns": ["Concern 1", "Concern 2", "Concern 3"],
            "news_triggers": [
                {{
                    "article_title": "Title of the news article",
                    "article_source": "Source of the article",
                    "article_date": "Date of the article",
                    "risk_connection": "How this article relates to legal liability risks"
                }}
            ]
        }}
    }},
    "overall_risk_assessment": {{
        "overall_risk_level": "Low/Medium/High/Critical",
        "summary": "Overall risk assessment summary",
        "critical_issues": ["Critical issue 1", "Critical issue 2"]
    }},
    "recommendations": [
        "Specific actionable recommendation 1",
        "Specific actionable recommendation 2",
        "Specific actionable recommendation 3",
        "Specific actionable recommendation 4",
        "Specific actionable recommendation 5"
    ],
    "next_steps": [
        "Immediate next step 1",
        "Immediate next step 2",
        "Immediate next step 3"
    ],
    "ai_confidence": 0.85,
    "analysis_timestamp": "{datetime.now().isoformat()}"
}}

Provide detailed, lawyer-style analysis with specific legal considerations and actionable recommendations. For each risk category identified, reference the specific news articles that triggered or influenced that risk assessment.
"""

        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a legal intelligence AI assistant specializing in business risk assessment for General Counsels. Always respond with valid JSON in the exact format requested."},
                    {"role": "user", "content": general_analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            
            # Extract the response content
            ai_response = response.choices[0].message.content.strip()
            
            # Try to parse as JSON
            try:
                result = json.loads(ai_response)
            except json.JSONDecodeError as e:
                print(f"JSON decode error for general analysis: {e}")
                print(f"Raw AI response was: {ai_response}")
                # If JSON parsing fails, create a structured response
                result = {
                    "error": "Failed to parse AI response as JSON",
                    "raw_response": ai_response,
                    "risk_analysis": {
                        "regulatory_compliance": {"risk_level": "Unknown", "assessment": "Analysis failed to parse properly", "key_concerns": ["General"]},
                        "operational_risks": {"risk_level": "Unknown", "assessment": "Analysis failed to parse properly", "key_concerns": ["General"]},
                        "financial_exposure": {"risk_level": "Unknown", "assessment": "Analysis failed to parse properly", "key_concerns": ["General"]},
                        "reputation_management": {"risk_level": "Unknown", "assessment": "Analysis failed to parse properly", "key_concerns": ["General"]},
                        "legal_liabilities": {"risk_level": "Unknown", "assessment": "Analysis failed to parse properly", "key_concerns": ["General"]}
                    },
                    "overall_risk_assessment": {
                        "overall_risk_level": "Unknown",
                        "summary": "Analysis failed to parse properly",
                        "critical_issues": ["Review raw response"]
                    },
                    "recommendations": ["Review the raw analysis response"],
                    "next_steps": ["Contact technical support"],
                    "ai_confidence": 0.5,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            result = {
                "error": f"Failed to analyze company: {str(e)}",
                "risk_analysis": {
                    "regulatory_compliance": {"risk_level": "Unknown", "assessment": "Analysis failed due to API error", "key_concerns": ["General"]},
                    "operational_risks": {"risk_level": "Unknown", "assessment": "Analysis failed due to API error", "key_concerns": ["General"]},
                    "financial_exposure": {"risk_level": "Unknown", "assessment": "Analysis failed due to API error", "key_concerns": ["General"]},
                    "reputation_management": {"risk_level": "Unknown", "assessment": "Analysis failed due to API error", "key_concerns": ["General"]},
                    "legal_liabilities": {"risk_level": "Unknown", "assessment": "Analysis failed due to API error", "key_concerns": ["General"]}
                },
                "overall_risk_assessment": {
                    "overall_risk_level": "Unknown",
                    "summary": "Analysis failed due to API error",
                    "critical_issues": ["Check OpenAI API configuration"]
                },
                "recommendations": ["Check OpenAI API configuration"],
                "next_steps": ["Verify API key and network connection"],
                "ai_confidence": 0.0,
                "analysis_timestamp": datetime.now().isoformat()
            }

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
