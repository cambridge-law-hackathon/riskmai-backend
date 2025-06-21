from flask import Blueprint, request, jsonify
from services.firebase_service import add_company as add_company_service, add_company_context as add_company_context_service, get_company_data as get_company_data_service
from services.firebase_service import get_all_companies as get_all_companies_service

companies_bp = Blueprint('companies', __name__)

@companies_bp.route('/companies', methods=['POST'])
def add_company():
    data = request.get_json()
    if not data or not 'name' in data:
        return jsonify({"error": "Company name is required"}), 400
    
    name = data.get('name')
    context = data.get('context', '') # context is optional

    company_id, error = add_company_service(name, context)

    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({"message": "Company added successfully", "company_id": company_id}), 201

@companies_bp.route('/companies/<company_id>/context', methods=['POST'])
def add_company_context(company_id):
    data = request.get_json()
    if not data or not 'context' in data:
        return jsonify({"error": "Context is required"}), 400
    
    context = data.get('context')

    _, error = add_company_context_service(company_id, context)

    if error:
        return jsonify({"error": error}), 500
    
    return jsonify({"message": "Context added successfully", "company_id": company_id}), 201

@companies_bp.route('/companies/<company_id>', methods=['GET'])
def get_company(company_id):
    """Get company data including context and documents for debugging"""
    company_data, error = get_company_data_service(company_id)
    
    if error:
        return jsonify({"error": error}), 500
    
    if not company_data:
        return jsonify({"error": "Company not found"}), 404
    
    return jsonify(company_data), 200

@companies_bp.route('/companies', methods=['GET'])
def get_companies():
    """Get a list of all companies (id and name)"""
    companies, error = get_all_companies_service()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(companies), 200 