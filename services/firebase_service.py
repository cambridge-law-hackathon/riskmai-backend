import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

load_dotenv()

# IMPORTANT: Security Best Practices
# 1. Use Workload Identity Federation instead of service account keys
# 2. Never commit credentials to version control
# 3. Use environment variables for configuration
# 4. Implement proper access controls

try:
    # Use Application Default Credentials (ADC) for secure authentication
    # This works with Workload Identity Federation, service accounts, or local development
    firebase_admin.initialize_app()
    
    db = firestore.client()
    print("Firebase connected successfully using secure authentication")

except Exception as e:
    print(f"Error initializing Firebase: {e}")
    db = None


def add_company(name, context):
    if not db:
        return None, "Firestore is not initialized."
    try:
        company_ref = db.collection('companies').document()
        company_ref.set({
            'name': name,
            'context': [context] if context else [],
            'created_at': firestore.SERVER_TIMESTAMP
        })
        return company_ref.id, None
    except Exception as e:
        return None, str(e)


def add_company_context(company_id, context):
    if not db:
        return None, "Firestore is not initialized."
    try:
        company_ref = db.collection('companies').document(company_id)
        company_ref.update({
            'context': firestore.ArrayUnion([context])
        })
        return company_id, None
    except Exception as e:
        return None, str(e)


def add_document_to_company(company_id, file_name, gcs_url, content, file_type="pdf"):
    if not db:
        return None, "Firestore is not initialized."
    try:
        doc_ref = db.collection('companies').document(company_id).collection('documents').document()
        doc_ref.set({
            'file_name': file_name,
            'gcs_url': gcs_url,
            'content': content,
            'file_type': file_type,
            'uploaded_at': firestore.SERVER_TIMESTAMP
        })
        return doc_ref.id, None
    except Exception as e:
        return None, str(e)


def get_company_data(company_id):
    if not db:
        return None, "Firestore is not initialized."
    try:
        company_ref = db.collection('companies').document(company_id)
        company_snapshot = company_ref.get()

        if not company_snapshot.exists:
            return None, None # Company not found

        company_data = company_snapshot.to_dict()
        company_data['id'] = company_snapshot.id

        # Get documents
        docs_ref = company_ref.collection('documents')
        docs = docs_ref.stream()
        
        company_data['documents'] = []
        for doc in docs:
            company_data['documents'].append(doc.to_dict())

        return company_data, None
    except Exception as e:
        return None, str(e)


def get_all_companies():
    if not db:
        return None, "Firestore is not initialized."
    try:
        companies_ref = db.collection('companies')
        companies = []
        for doc in companies_ref.stream():
            data = doc.to_dict()
            companies.append({
                'id': doc.id,
                'name': data.get('name', '')
            })
        return companies, None
    except Exception as e:
        return None, str(e)


def store_analysis_result(company_id, analysis_type, payload, result, timestamp):
    """
    Store analysis results in the database.
    
    Args:
        company_id: ID of the company
        analysis_type: Type of analysis ("general" or "dynamic_risk")
        payload: The data sent to the AI service
        result: The response from the AI service
        timestamp: When the analysis was performed
    
    Returns:
        tuple: (analysis_id, error)
    """
    if not db:
        return None, "Firestore is not initialized."
    try:
        analysis_ref = db.collection('companies').document(company_id).collection('analyses').document()
        analysis_ref.set({
            'analysis_type': analysis_type,
            'payload': payload,
            'result': result,
            'timestamp': timestamp,
            'created_at': firestore.SERVER_TIMESTAMP
        })
        return analysis_ref.id, None
    except Exception as e:
        return None, str(e)


def get_company_analyses(company_id, analysis_id=None, analysis_type=None, limit=10):
    """
    Get analysis results for a company.
    
    Args:
        company_id: ID of the company
        analysis_id: Optional specific analysis ID
        analysis_type: Optional filter by analysis type
        limit: Maximum number of results to return
    
    Returns:
        tuple: (analyses_list, error)
    """
    if not db:
        return None, "Firestore is not initialized."
    try:
        analyses_ref = db.collection('companies').document(company_id).collection('analyses')
        
        # Build query
        query = analyses_ref
        
        if analysis_type:
            query = query.where('analysis_type', '==', analysis_type)
        
        # Order by timestamp (newest first)
        query = query.order_by('timestamp', direction=firestore.Query.DESCENDING)
        
        # Limit results
        query = query.limit(limit)
        
        analyses = []
        for doc in query.stream():
            analysis_data = doc.to_dict()
            analysis_data['id'] = doc.id
            analyses.append(analysis_data)
        
        # If specific analysis_id requested, filter results
        if analysis_id:
            analyses = [a for a in analyses if a['id'] == analysis_id]
        
        return analyses, None
    except Exception as e:
        return None, str(e)


def get_analysis_by_id(company_id, analysis_id):
    """
    Get a specific analysis result by ID.
    
    Args:
        company_id: ID of the company
        analysis_id: ID of the analysis
    
    Returns:
        tuple: (analysis_data, error)
    """
    if not db:
        return None, "Firestore is not initialized."
    try:
        analysis_ref = db.collection('companies').document(company_id).collection('analyses').document(analysis_id)
        analysis_snapshot = analysis_ref.get()
        
        if not analysis_snapshot.exists:
            return None, None  # Analysis not found
        
        analysis_data = analysis_snapshot.to_dict()
        analysis_data['id'] = analysis_snapshot.id
        
        return analysis_data, None
    except Exception as e:
        return None, str(e) 