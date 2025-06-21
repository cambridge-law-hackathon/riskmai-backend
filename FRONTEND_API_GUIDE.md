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

### 6. **Analyze a Company**

- **POST** `/api/companies/{company_id}/analyse`
- **Body:** (empty or `{}`)
- **Response:**  
  ```json
  {
    "company_info": { ... },
    "analysis_summary": "...",
    "risk_factors": [ ... ],
    "recommendations": [ ... ],
    "available_data": { ... }
  }
  ```

---

### 7. **Analyse Dynamic Risk**

- **POST** `/api/companies/{company_id}/dynamic-risk`
- **Body:**
  ```json
  {
    "risk_description": "New GDPR regulations require immediate data processing changes",
    "risk_context": "*insert text from an email or link to a news article here*",
    "risk_type": "regulatory"
  }
  ```
- **Response:**
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
      "Immediately review contracts for force majeure clauses",
      "Assess regulatory reporting requirements",
      "Evaluate operational continuity plans"
    ],
    "next_steps": [
      "Schedule emergency board meeting",
      "Review insurance coverage",
      "Update risk register"
    ],
    "ai_confidence": 0.85,
    "analysis_timestamp": "2024-01-01T00:00:00Z"
  }
  ```

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
