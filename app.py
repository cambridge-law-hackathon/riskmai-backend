from flask import Flask, request
from flask_cors import CORS
from blueprints.companies import companies_bp
from blueprints.documents import documents_bp
from blueprints.analysis import analysis_bp
import os

app = Flask(__name__)

# CORS Configuration
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",  # React dev server
            "http://localhost:3001",  # Alternative React port
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "https://your-frontend-domain.com"  # Add your production frontend URL
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
        "supports_credentials": True
    }
})

# Security Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Register Blueprints
app.register_blueprint(companies_bp, url_prefix='/api')
app.register_blueprint(documents_bp, url_prefix='/api')
app.register_blueprint(analysis_bp, url_prefix='/api')

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # CORS headers for preflight requests
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', '*')
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 hours
    
    return response

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    # Security: Use HTTPS in production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=5001, host='127.0.0.1') 