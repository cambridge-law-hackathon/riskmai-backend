from flask import Blueprint, request, jsonify
from services import firebase_service

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
    
    # Create a summary of available data
    data_summary = {
        "company_name": company_name,
        "context_items_count": len(context_items),
        "documents_count": total_documents,
        "total_content_length": total_content_length,
        "context_items": context_items,
        "document_names": [doc.get('file_name', 'Unknown') for doc in documents]
    }

    # Here you would typically call the news searching AI agent
    # with company_data to get real analysis.
    
    # For now, provide a realistic analysis based on available data
    analysis_result = {
        "company_info": data_summary,
        "analysis_summary": f"Analysis completed for {company_name}. Found {len(context_items)} context items and {total_documents} documents with {total_content_length} characters of content.",
        "risk_factors": [
            {
                "factor": "Data Completeness", 
                "level": "Medium" if total_documents > 0 else "High", 
                "details": f"Company has {total_documents} documents and {len(context_items)} context items for analysis."
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
            "Integrate with news API for real-time risk assessment."
        ],
        "available_data": {
            "context_items": context_items,
            "document_count": total_documents,
            "content_available": total_content_length > 0
        }
    }

    return jsonify(analysis_result), 200 
