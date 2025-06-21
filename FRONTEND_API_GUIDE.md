# Frontend API Guide: Business Risk Analysis Platform

## Overview

This guide provides comprehensive documentation for integrating your frontend application with the Business Risk Analysis Platform. The API enables you to manage companies, upload legal documents, perform risk analysis, and retrieve analysis results.

## Quick Start

### Base URL
- **Development**: `http://127.0.0.1:5001/api`
- **Production**: `https://your-production-domain.com/api`

### Authentication
Currently, no authentication is required for development. For production, implement appropriate authentication mechanisms.

### Content Types
- **JSON**: `Content-Type: application/json`
- **File Uploads**: `Content-Type: multipart/form-data`

---

## API Endpoints

### 1. **Company Management**

#### List All Companies
- **GET** `/api/companies`
- **Description**: Retrieve all companies in the system
- **Response**:
  ```json
  [
    {
      "id": "abc123",
      "name": "Acme Corp"
    },
    {
      "id": "xyz789", 
      "name": "Globex Inc"
    }
  ]
  ```

#### Add Company
- **POST** `/api/companies`
- **Description**: Create a new company
- **Body**:
  ```json
  {
    "name": "Acme Corp",
    "context": "Acme is a global widget supplier with operations in 15 countries."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Company added successfully",
    "company_id": "abc123"
  }
  ```

#### Add Company Context
- **POST** `/api/companies/{company_id}/context`
- **Description**: Add additional context to an existing company
- **Body**:
  ```json
  {
    "context": "Acme recently expanded into European markets and acquired a competitor."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Context added successfully",
    "company_id": "abc123"
  }
  ```

#### Get Company Data
- **GET** `/api/companies/{company_id}`
- **Description**: Retrieve complete company data including context and documents
- **Response**:
  ```json
  {
    "id": "abc123",
    "name": "Acme Corp",
    "context": [
      "Acme is a global widget supplier with operations in 15 countries.",
      "Acme recently expanded into European markets and acquired a competitor."
    ],
    "created_at": "2024-01-15T10:00:00Z",
    "documents": [
      {
        "file_name": "master_service_agreement.pdf",
        "gcs_url": "https://storage.googleapis.com/bucket/abc123/master_service_agreement.pdf",
        "content": "This Master Service Agreement (MSA) is entered into...",
        "file_type": "pdf",
        "uploaded_at": "2024-01-15T11:00:00Z"
      }
    ]
  }
  ```

### 2. **Document Management**

#### Upload Document
- **POST** `/api/companies/{company_id}/documents`
- **Description**: Upload PDF or EML files for analysis
- **Content-Type**: `multipart/form-data`
- **Body**: Form data with `file` field
- **Supported Formats**: PDF, EML (email files)
- **Response**:
  ```json
  {
    "message": "File uploaded and processed successfully",
    "document_id": "doc456",
    "file_type": "pdf"
  }
  ```

**Frontend Implementation Example:**
```javascript
const uploadDocument = async (companyId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(`/api/companies/${companyId}/documents`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};
```

### 3. **Risk Analysis**

#### General Company Analysis
- **POST** `/api/companies/{company_id}/analyse`
- **Description**: Perform general risk analysis on company data
- **Body**: Empty object or `{}`
- **Response**:
  ```json
  {
    "analysis_id": "analysis_789",
    "risk_factors": [
      {
        "severity": "Medium",
        "risk_type": "Operational Risk",
        "specific_event": "Supply Chain Disruption",
        "affected_contracts": "supplier_agreement.pdf",
        "affected_clauses": "Force Majeure",
        "narrative": {
          "solutions_in_contract": "Contract includes force majeure provisions.",
          "alternative_mitigation_strategies": "Diversify suppliers and increase inventory.",
          "monitoring_tasks": "Monitor supplier performance monthly."
        }
      }
    ],
    "available_data": {
      "context_items": ["Company context information"],
      "document_count": 3,
      "content_available": true,
      "news_available": true
    }
  }
  ```

#### Dynamic Risk Analysis
- **POST** `/api/companies/{company_id}/analyse`
- **Description**: Analyze specific risk scenarios
- **Body**:
  ```json
  {
    "risk_description": "New GDPR regulations require immediate data processing changes",
    "risk_context": "EU just announced stricter requirements affecting our customer data handling",
    "risk_type": "regulatory"
  }
  ```
- **Response**:
  ```json
  {
    "analysis_id": "analysis_790",
    "risk_analysis": {
      "scenario": "New GDPR regulations require immediate data processing changes",
      "risk_level": "High",
      "impact_assessment": "This regulatory risk represents an existential threat to company operations...",
      "affected_areas": [
        "Contractual obligations and SLA compliance",
        "Customer relationship management and retention",
        "Financial stability and cash flow"
      ]
    },
    "news_analysis": {
      "articles_found": 15,
      "negative_sentiment_ratio": 0.4,
      "trending_topics": ["GDPR compliance", "Data protection", "Regulatory changes"],
      "market_context": "Found 15 relevant articles with 6 showing negative sentiment"
    },
    "company_specific_insights": {
      "relevant_contracts": 3,
      "context_alignment": "High",
      "data_coverage": "Comprehensive",
      "critical_contracts_identified": "Multiple customer contracts with data processing clauses",
      "force_majeure_analysis": "Regulatory changes may trigger force majeure provisions"
    },
    "recommendations": [
      "Immediate Legal Response: Engage outside counsel specializing in data protection...",
      "Customer Communication Strategy: Develop a comprehensive communication plan...",
      "Compliance Planning: Immediately initiate GDPR compliance assessment..."
    ],
    "next_steps": [
      "Executive Crisis Management: Convene an emergency board meeting within 24 hours...",
      "Financial Risk Mitigation: Immediately review all insurance policies...",
      "Regulatory and Compliance Review: Conduct immediate review of all regulatory obligations..."
    ],
    "ai_confidence": 0.92,
    "analysis_timestamp": "2024-01-15T12:00:00Z"
  }
  ```

### 4. **Analysis Results**

#### Get All Company Analyses
- **GET** `/api/companies/{company_id}/analyses`
- **Description**: Retrieve all analysis results for a company
- **Query Parameters**:
  - `analysis_type`: Filter by "general" or "dynamic_risk"
  - `limit`: Maximum results (default: 10)
- **Response**:
  ```json
  [
    {
      "id": "analysis_789",
      "analysis_type": "dynamic_risk",
      "payload": {
        "company_info": { ... },
        "news_data": { ... },
        "risk_scenario": { ... }
      },
      "result": {
        "risk_analysis": { ... },
        "recommendations": [ ... ],
        "next_steps": [ ... ],
        "ai_confidence": 0.92,
        "analysis_timestamp": "2024-01-15T12:00:00Z"
      },
      "timestamp": "2024-01-15T12:00:00Z",
      "created_at": "2024-01-15T12:00:00Z"
    }
  ]
  ```

#### Get Specific Analysis
- **GET** `/api/companies/{company_id}/analyses/{analysis_id}`
- **Description**: Retrieve a specific analysis result
- **Response**:
  ```json
  {
    "id": "analysis_789",
    "analysis_type": "dynamic_risk",
    "payload": {
      "company_info": {
        "name": "Acme Corp",
        "context": ["Company context"],
        "documents": [
          {
            "file_name": "contract.pdf",
            "content": "Contract content...",
            "file_type": "pdf"
          }
        ]
      },
      "news_data": {
        "articles_summary": [
          {
            "title": "News title",
            "description": "News description",
            "content": "News content",
            "url": "https://example.com",
            "source": "Reuters",
            "date": "2024-01-15T10:00:00Z",
            "sentiment": "negative"
          }
        ]
      },
      "risk_scenario": {
        "description": "Risk description",
        "context": "Risk context",
        "type": "regulatory",
        "timestamp": "2024-01-15T12:00:00Z"
      }
    },
    "result": {
      "risk_analysis": { ... },
      "recommendations": [ ... ],
      "next_steps": [ ... ],
      "ai_confidence": 0.92,
      "analysis_timestamp": "2024-01-15T12:00:00Z"
    },
    "timestamp": "2024-01-15T12:00:00Z",
    "created_at": "2024-01-15T12:00:00Z"
  }
  ```

---

## Frontend Implementation Examples

### React Hook for API Calls

```javascript
import { useState, useCallback } from 'react';

const useBusinessRiskAPI = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const apiCall = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`/api${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { apiCall, loading, error };
};
```

### Company Management Component

```javascript
import React, { useState, useEffect } from 'react';
import { useBusinessRiskAPI } from './hooks/useBusinessRiskAPI';

const CompanyManager = () => {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState(null);
  const { apiCall, loading, error } = useBusinessRiskAPI();

  // Load companies
  useEffect(() => {
    const loadCompanies = async () => {
      try {
        const data = await apiCall('/companies');
        setCompanies(data);
      } catch (err) {
        console.error('Failed to load companies:', err);
      }
    };
    loadCompanies();
  }, [apiCall]);

  // Add company
  const addCompany = async (name, context) => {
    try {
      const result = await apiCall('/companies', {
        method: 'POST',
        body: JSON.stringify({ name, context })
      });
      
      // Reload companies
      const updatedCompanies = await apiCall('/companies');
      setCompanies(updatedCompanies);
      
      return result.company_id;
    } catch (err) {
      console.error('Failed to add company:', err);
    }
  };

  return (
    <div>
      <h2>Companies</h2>
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      
      <ul>
        {companies.map(company => (
          <li key={company.id} onClick={() => setSelectedCompany(company.id)}>
            {company.name}
          </li>
        ))}
      </ul>
    </div>
  );
};
```

### Document Upload Component

```javascript
import React, { useState } from 'react';
import { useBusinessRiskAPI } from './hooks/useBusinessRiskAPI';

const DocumentUpload = ({ companyId }) => {
  const [uploading, setUploading] = useState(false);
  const { apiCall, error } = useBusinessRiskAPI();

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setUploading(true);
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      await apiCall(`/companies/${companyId}/documents`, {
        method: 'POST',
        headers: {}, // Let browser set Content-Type for FormData
        body: formData
      });
      
      alert('Document uploaded successfully!');
    } catch (err) {
      console.error('Upload failed:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h3>Upload Document</h3>
      <input
        type="file"
        accept=".pdf,.eml"
        onChange={handleFileUpload}
        disabled={uploading}
      />
      {uploading && <p>Uploading...</p>}
      {error && <p>Error: {error}</p>}
    </div>
  );
};
```

### Risk Analysis Component

```javascript
import React, { useState } from 'react';
import { useBusinessRiskAPI } from './hooks/useBusinessRiskAPI';

const RiskAnalysis = ({ companyId }) => {
  const [analysisType, setAnalysisType] = useState('general');
  const [riskData, setRiskData] = useState({});
  const [analysisResult, setAnalysisResult] = useState(null);
  const { apiCall, loading, error } = useBusinessRiskAPI();

  const runAnalysis = async () => {
    try {
      let body = {};
      
      if (analysisType === 'dynamic_risk') {
        body = {
          risk_description: riskData.description,
          risk_context: riskData.context,
          risk_type: riskData.type
        };
      }
      
      const result = await apiCall(`/companies/${companyId}/analyse`, {
        method: 'POST',
        body: JSON.stringify(body)
      });
      
      setAnalysisResult(result);
    } catch (err) {
      console.error('Analysis failed:', err);
    }
  };

  return (
    <div>
      <h3>Risk Analysis</h3>
      
      <div>
        <label>
          Analysis Type:
          <select value={analysisType} onChange={(e) => setAnalysisType(e.target.value)}>
            <option value="general">General Analysis</option>
            <option value="dynamic_risk">Dynamic Risk Analysis</option>
          </select>
        </label>
      </div>

      {analysisType === 'dynamic_risk' && (
        <div>
          <input
            placeholder="Risk Description"
            value={riskData.description || ''}
            onChange={(e) => setRiskData({...riskData, description: e.target.value})}
          />
          <input
            placeholder="Risk Context"
            value={riskData.context || ''}
            onChange={(e) => setRiskData({...riskData, context: e.target.value})}
          />
          <input
            placeholder="Risk Type"
            value={riskData.type || ''}
            onChange={(e) => setRiskData({...riskData, type: e.target.value})}
          />
        </div>
      )}

      <button onClick={runAnalysis} disabled={loading}>
        {loading ? 'Analyzing...' : 'Run Analysis'}
      </button>

      {error && <p>Error: {error}</p>}

      {analysisResult && (
        <div>
          <h4>Analysis Results</h4>
          <pre>{JSON.stringify(analysisResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};
```

---

## Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid data)
- **404**: Not Found (company/analysis not found)
- **500**: Internal Server Error

### Error Response Format
```json
{
  "error": "Description of the error"
}
```

### Frontend Error Handling
```javascript
const handleAPIError = (error, context) => {
  if (error.status === 404) {
    console.error(`${context} not found`);
    // Handle not found
  } else if (error.status === 400) {
    console.error(`Invalid data: ${error.message}`);
    // Handle validation errors
  } else {
    console.error(`API error: ${error.message}`);
    // Handle general errors
  }
};
```

---

## Best Practices

### 1. **State Management**
- Store company IDs and analysis IDs in your app state
- Cache analysis results to avoid unnecessary API calls
- Implement loading states for better UX

### 2. **File Uploads**
- Validate file types before upload (PDF, EML only)
- Show upload progress
- Handle large files appropriately

### 3. **Error Handling**
- Implement retry logic for failed requests
- Show user-friendly error messages
- Log errors for debugging

### 4. **Performance**
- Implement pagination for large datasets
- Use query parameters to filter results
- Cache frequently accessed data

### 5. **Security**
- Validate all user inputs
- Sanitize data before sending to API
- Implement proper CORS configuration

---

## Development Workflow

### 1. **Setup**
```bash
# Start the backend server
cd business-risk
poetry run python app.py
```

### 2. **Testing**
- Use the provided Postman collection for API testing
- Test all endpoints with various data scenarios
- Verify error handling

### 3. **Integration**
- Start with simple API calls
- Gradually add complex features
- Test with real data

---

## Support

For questions or issues:
- Check the API documentation
- Review error messages carefully
- Test with Postman collection
- Contact the backend team

---

**Note**: This API is designed to be simple and flexible. All responses are JSON, and the structure is consistent across endpoints. 