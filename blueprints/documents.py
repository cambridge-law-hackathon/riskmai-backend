from flask import Blueprint, request, jsonify
from services import gcs_service, firebase_service
import fitz # PyMuPDF
from eml_parser import EmlParser
import os

documents_bp = Blueprint('documents', __name__)

def extract_email_content(file):
    """Extract text content from .eml file using eml-parser"""
    # Parse the email using eml-parser
    parser = EmlParser()
    email_data = parser.decode_email_bytes(file.read())
    
    # Extract headers
    subject = email_data.get('header', {}).get('subject', [''])[0] if email_data.get('header', {}).get('subject') else ''
    sender = email_data.get('header', {}).get('from', [''])[0] if email_data.get('header', {}).get('from') else ''
    recipients = email_data.get('header', {}).get('to', [''])[0] if email_data.get('header', {}).get('to') else ''
    date = email_data.get('header', {}).get('date', [''])[0] if email_data.get('header', {}).get('date') else ''
    
    # Get email body
    body = ""
    if 'body' in email_data:
        for part in email_data['body']:
            if part.get('content_type') == 'text/plain':
                body += part.get('content', '')
            elif part.get('content_type') == 'text/html':
                # For HTML content, we'll use the plain text version if available
                # or extract text from HTML
                html_content = part.get('content', '')
                if html_content:
                    # Simple HTML tag removal - in production you might want to use BeautifulSoup
                    import re
                    clean_text = re.sub(r'<[^>]+>', '', html_content)
                    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                    body += clean_text
    
    return {
        'subject': subject,
        'sender': sender,
        'recipients': recipients,
        'date': date,
        'body': body,
        'full_content': f"Subject: {subject}\nFrom: {sender}\nTo: {recipients}\nDate: {date}\n\n{body}"
    }

@documents_bp.route('/companies/<company_id>/documents', methods=['POST'])
def upload_document(company_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.endswith('.pdf') or file.filename.endswith('.eml')):
        try:
            # 1. Upload to GCS
            gcs_path = f"{company_id}/{file.filename}"
            public_url, error = gcs_service.upload_file(file, gcs_path)
            if error:
                return jsonify({"error": f"GCS upload failed: {error}"}), 500

            # 2. Extract text based on file type
            file.seek(0) # reset file pointer
            
            if file.filename.endswith('.pdf'):
                # Extract text from PDF
                pdf_document = fitz.open(stream=file.read(), filetype="pdf")
                text = ""
                for page in pdf_document:
                    text += page.get_text()
                file_type = "pdf"
                
            elif file.filename.endswith('.eml'):
                # Extract text from email
                email_data = extract_email_content(file)
                text = email_data['body']
                file_type = "email"
            
            # 3. Save document info to Firebase
            doc_id, error = firebase_service.add_document_to_company(
                company_id=company_id,
                file_name=file.filename,
                gcs_url=public_url,
                content=text,
                file_type=file_type
            )
            if error:
                return jsonify({"error": f"Failed to save document to firestore: {error}"}), 500

            return jsonify({
                "message": "File uploaded and processed successfully",
                "document_id": doc_id,
                "file_type": file_type
            }), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({"error": "Invalid file type, only PDF and EML files are accepted."}), 400 