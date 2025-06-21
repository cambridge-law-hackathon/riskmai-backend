# Frontend Integration Guide: Business Risk API

## Overview

This backend provides a set of RESTful JSON APIs for managing companies, uploading documents (PDFs and emails), and running risk analysis. You'll be building a React frontend to interact with these endpoints.

---

## API Base URL

- **Local development:**  
  `http://127.0.0.1:5001/api`

---

## Authentication

- **No authentication is required for local development** (unless you add it).
- For production, we would want to add authentication (e.g., Google OAuth, Auth0, etc.).

---

## Endpoints

### 1. **List All Companies**

- **GET** `/api/companies`
- **Response:**
  ```json
  [
    { "id": "abc123", "name": "Acme Corp" },
    { "id": "xyz789", "name": "Globex Inc." }
  ]
  ```
- **Usage:**
  - Use this endpoint to populate a dropdown or list of companies in your React app.

---

### 2. **Add a Company**

- **POST** `/api/companies`
- **Body:**  
  ```json
  {
    "name": "Acme Corp",
    "context": "Acme is a global widget supplier."
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Company added successfully",
    "company_id": "abc123"
  }
  ```

---

### 3. **Add Company Context**

- **POST** `/api/companies/{company_id}/context`
- **Body:**  
  ```json
  {
    "context": "Acme recently expanded into Europe."
  }
  ```
- **Response:**  
  ```json
  {
    "message": "Context added successfully",
    "company_id": "abc123"
  }
  ```

---

### 4. **Upload a Document (PDF or EML)**

- **POST** `/api/companies/{company_id}/documents`
- **Form Data:**  
  - `file`: (PDF or EML file)
- **Response:**  
  ```json
  {
    "message": "File uploaded and processed successfully",
    "document_id": "doc456",
    "file_type": "pdf" // or "email"
  }
  ```

**React Example:**
```js
const formData = new FormData();
formData.append('file', fileInput.files[0]);
fetch('/api/companies/abc123/documents', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

### 5. **Get Company Data**

- **GET** `/api/companies/{company_id}`
- **Response:**  
  ```json
  {
    "id": "abc123",
    "name": "Acme Corp",
    "context": ["Acme is a global widget supplier.", "Acme recently expanded into Europe."],
    "created_at": "...",
    "documents": [
      {
        "file_name": "contract.pdf",
        "gcs_url": "https://storage.googleapis.com/...",
        "content": "Extracted text...",
        "file_type": "pdf",
        "uploaded_at": "..."
      }
    ]
  }
  ```

---
### 6. **Analyse a Company (Unified Endpoint)**

- **POST** `/api/companies/{company_id}/analyse`
- **For General Analysis (Body):**  
  ```json
  {}
  ```
  or empty body
- **For Dynamic Risk Analysis (Body):**
  ```json
  {
    "risk_description": "New GDPR regulations require immediate data processing changes",
    "risk_context": "*insert text from an email or link to a news article here*",
    "risk_type": "regulatory"
  }
  ```
- **General Analysis Response:**  
  ```json
  {
    "risk_factors": [
      {
        "severity": "Low",
        "risk_type": "Reputational Risk",
        "affected_contracts": "contract.pdf",
        "affected_clauses": "Clause 1.1",
        "narrative": {
          "solutions_in_contract": "The contract does have a clause that addresses this risk. 16.1",
          "alternative_mitigations": "Do xyz to mitigate the risk.",
          "monitoring_tasks": "Monitor the risk and report to the board every 3 months."
        }
      }
    ],
    "available_data": {
      "context_items": ["Acme is a global widget supplier."],
      "document_count": 3,
      "content_available": true,
      "news_available": true
    }
  }
  ```
- **Dynamic Risk Analysis Response:**
  ```json
  {
    "risk_analysis": {
      "scenario": "New GDPR regulations require immediate data processing changes",
      "risk_level": "High",
      "impact_assessment": "This regulatory risk could significantly impact Acme Corp's operations.",
      "affected_areas": ["Contractual obligations", "Regulatory compliance", "Operational processes"]
    },
    "company_specific_insights": {
      "relevant_contracts": 3,
      "context_alignment": "High",
      "data_coverage": "Comprehensive"
    },
    "recommendations": [
      "Immediate Legal Response: Engage outside counsel specializing in cloud infrastructure disputes...",
      "Customer Communication Strategy: Develop a comprehensive communication plan...",
      "Infrastructure Migration Planning: Immediately initiate parallel infrastructure deployment..."
    ],
    "next_steps": [
      "Executive Crisis Management: Convene an emergency board meeting within 24 hours...",
      "Financial Risk Mitigation: Immediately review all insurance policies...",
      "Regulatory and Compliance Review: Conduct immediate review of all regulatory obligations..."
    ],
    "ai_confidence": 0.92,
    "analysis_timestamp": "2024-01-01T00:00:00Z"
  }
  ```

---

## Response Format Details

### General Analysis Response Fields

**`risk_factors`** - Array of identified risk factors:
- `severity`: Risk level ("Low", "Medium", "High", "Critical")
- `risk_type`: Category of risk ("Reputational Risk", "Operational Risk", "Financial Risk", etc.)
- `affected_contracts`: Specific contracts impacted by this risk
- `affected_clauses`: Specific contract clauses related to the risk
- `narrative`: Detailed analysis including:
  - `solutions_in_contract`: How the contract addresses (or fails to address) the risk
  - `alternative_mitigations`: Suggested actions to mitigate the risk
  - `monitoring_tasks`: Ongoing monitoring requirements

**`available_data`** - Summary of data used in analysis:
- `context_items`: Array of company context information
- `document_count`: Number of documents analyzed
- `content_available`: Boolean indicating if document content was available
- `news_available`: Boolean indicating if news data was available

### Dynamic Risk Analysis Response Fields

**`risk_analysis`** - Core risk assessment:
- `scenario`: Description of the specific risk scenario
- `risk_level`: Overall risk level assessment
- `impact_assessment`: Detailed impact analysis
- `affected_areas`: Business areas impacted by the risk

**`news_analysis`** - News sentiment and trend analysis:
- `articles_found`: Number of relevant news articles
- `negative_sentiment_ratio`: Proportion of negative sentiment articles
- `trending_topics`: Key topics from recent news
- `market_context`: Summary of market conditions

**`company_specific_insights`** - Company-specific analysis:
- `relevant_contracts`: Number of contracts relevant to the risk
- `context_alignment`: How well company context aligns with the risk
- `data_coverage`: Quality of available data for analysis
- `critical_contracts_identified`: Specific contracts of concern
- `force_majeure_analysis`: Analysis of force majeure implications

**`recommendations`** - Detailed action recommendations with legal context

**`next_steps`** - Immediate action items with executive-level guidance

**`ai_confidence`** - Confidence score (0-1) for the analysis quality

**`analysis_timestamp`** - When the analysis was performed

---

## File Upload Tips

- Use `FormData` for file uploads.
- Only PDF and EML files are accepted.
- The backend will extract and store the text content.

---

## Error Handling

- All errors are returned as JSON:
  ```json
  { "error": "Description of the error" }
  ```
- Check for HTTP status codes (e.g., 400, 404, 500).

---

## CORS

- If you run React on a different port (e.g., `localhost:3000`), you may need to enable CORS in the Flask backend for development.
- Ask the backend team to add CORS support if you get CORS errors.

---

## Example Workflow

1. **Create a company**  
   → Save the returned `company_id`
2. **Add context**  
   → POST more context as needed
3. **Upload documents**  
   → POST PDFs or EMLs
4. **Get company data**  
   → GET to display all info
5. **Analyze company**  
   → POST to `/analyse` and display results

---

## Questions?

- If you need new endpoints or changes, talk to the backend team.
- For authentication, CORS, or deployment, coordinate with the backend.
