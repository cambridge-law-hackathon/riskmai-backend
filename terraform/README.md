# Infrastructure as Code - Business Risk Platform

This directory contains Terraform configurations to set up the required Google Cloud infrastructure for the Business Risk Analysis platform.

## What This Creates

- **Google Cloud Storage Bucket**: For storing uploaded documents (PDFs and emails)
- **Firebase Project**: For the application database
- **Firestore Database**: For storing company data, context, and document metadata
- **Service Account**: With appropriate permissions for the application
- **IAM Roles**: Proper access controls for security

## Prerequisites

1. **Google Cloud CLI** installed and authenticated:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Terraform** installed (version >= 1.0):
   ```bash
   # For Ubuntu/Debian
   wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
   sudo apt update && sudo apt install terraform
   ```

3. **Google Cloud Project** with billing enabled

## Setup Instructions

### 1. Configure Variables

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
```

Edit `terraform.tfvars` and set your project ID:
```hcl
project_id = "your-actual-project-id"
```

### 2. Initialize Terraform

```bash
terraform init
```

### 3. Review the Plan

```bash
terraform plan
```

This will show you what resources will be created. Review the output carefully.

### 4. Apply the Configuration

```bash
terraform apply
```

When prompted, type `yes` to confirm.

### 5. Get Output Values

After successful deployment, Terraform will output important information:

```bash
terraform output
```

## Output Values

- `bucket_name`: Your GCS bucket name
- `firebase_project_id`: Your Firebase project ID
- `service_account_email`: Service account email for the app
- `service_account_key_path`: Path to the service account key

## Update Your Environment

After deployment, update your `.env` file with the output values:

```bash
# Copy the bucket name from terraform output
GCS_BUCKET_NAME="your-bucket-name-from-output"

# For local development, you can use Application Default Credentials
# or set the service account key path if needed
```

## Security Features

- **Uniform bucket-level access**: Prevents accidental public access
- **Versioning**: Protects against accidental deletions
- **Lifecycle rules**: Automatically manages old files
- **Least privilege**: Service account has only necessary permissions
- **Labels**: For better resource organization

## Cleanup

To destroy all created resources:

```bash
terraform destroy
```

⚠️ **Warning**: This will delete all data in the bucket and Firestore database!

## Troubleshooting

### Common Issues

1. **API not enabled**: Run `terraform apply` again after enabling APIs
2. **Permission denied**: Ensure your account has the necessary roles
3. **Bucket name taken**: Change the `bucket_name` variable

### Getting Help

- Check the [Terraform Google Provider documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- Review the [Google Cloud IAM documentation](https://cloud.google.com/iam/docs)

## Production Considerations

For production deployment:

1. Remove `force_destroy = true` from the bucket configuration
2. Adjust lifecycle rules based on your retention requirements
3. Consider using Workload Identity Federation instead of service account keys
4. Enable audit logging for all services
5. Set up monitoring and alerting 