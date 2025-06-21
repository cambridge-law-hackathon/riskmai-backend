# Business Risk Analysis API

This is a Flask-based backend for a legal intelligence tool designed to help General Counsels assess business risks.

## Features

- **Company Management**: Add companies and related context.
- **Document Processing**: Upload PDF documents, extract text, and store securely.
- **Risk Analysis**: Placeholder for a sophisticated analysis engine. A separate AI agent will do the work here and return us the results.

## Project Structure

```
.
├── app.py              # Main Flask application
├── blueprints          # API endpoints organized by resource
│   ├── __init__.py
│   ├── analysis.py
│   ├── companies.py
│   └── documents.py
├── pyproject.toml      # Poetry configuration and dependencies
├── services            # Modules for external services
│   ├── __init__.py
│   ├── firebase_service.py
│   └── gcs_service.py
└── .gitignore
```

## Setup and Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd business-risk
    ```

2.  **Install Poetry (if not already installed)**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3.  **Install dependencies using Poetry**
    ```bash
    poetry install
    ```

4.  **Set up Google Cloud Services with Secure Authentication**
    - Create a Firebase project at [https://console.firebase.google.com/](https://console.firebase.google.com/).
    - Create a Google Cloud Storage bucket with proper IAM roles.
    - **For Local Development**: Run `gcloud auth application-default login`
    - **For Production**: Use Workload Identity Federation (recommended)
    - Create a `.env` file in the root directory and add:
      ```
      GCS_BUCKET_NAME="your-gcs-bucket-name"
      ```

5.  **Run the application**
    ```bash
    poetry run python app.py
    ```
    The server will start on `http://127.0.0.1:5001`.

## Security Best Practices

- **Authentication**: Use Workload Identity Federation or Application Default Credentials
- **Credentials**: Never commit service account keys or credentials to version control
- **Access Control**: Implement proper IAM roles and permissions
- **HTTPS**: Use HTTPS for all production communications
- **Input Validation**: Validate and sanitize all user inputs
- **Audit Logging**: Enable audit logs for all services
- **Environment Variables**: Use environment variables for all configuration
- **Dependencies**: Regularly update dependencies for security patches

## Development

- **Add a new dependency**: `poetry add package-name`
- **Add a development dependency**: `poetry add --group dev package-name`
- **Remove a dependency**: `poetry remove package-name`
- **Update dependencies**: `poetry update`
- **Activate virtual environment**: `poetry shell`

## API Endpoints

- `POST /api/companies`: Add a new company that the General Counsel is working with. This serves as an entity to tie context to.
  - Body: `{"name": "Company Name", "context": "Initial context"}`
- `GET /api/companies`: Get a list of all companies (id and name) for populating frontend lists.
- `GET /api/companies/<company_id>`: Get company data including context and documents. Used when analysing company data.
- `POST /api/companies/<company_id>/context`: Add context to a company. This will just be written text about who they are, what they do, etc.
  - Body: `{"context": "More context about the company"}`
- `POST /api/companies/<company_id>/documents`: Upload a PDF document. This will be scraped and stored in GCP whereas the scraped text will
be stored in firebase, enabling us to ingest a lot of context about a given company and their risk profile.
  - Body: `multipart/form-data` with a `file` field.
  - Supported file types: PDF and EML (email) files
- `POST /api/companies/<company_id>/analyze`: Analyze the company's risk profile. This will interact with the AI agent, sending the written context and document context for it to analyse that context for this given company with relevant news.
  - Returns analysis based on company context and document content.
- `POST /api/companies/<company_id>/dynamic-risk`: Analyze a specific dynamic risk scenario for a company.
  - Body: `{"risk_description": "Description of the risk", "risk_context": "Additional context", "risk_type": "regulatory"}`
  - Combines user-provided risk information with company context and documents for AI analysis of more dynamic risks.
