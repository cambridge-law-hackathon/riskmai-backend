from google.cloud import storage
import os
from dotenv import load_dotenv

load_dotenv()

# IMPORTANT: Security Best Practices
# 1. Use Workload Identity Federation or Application Default Credentials
# 2. Never commit credentials to version control
# 3. Use environment variables for configuration
# 4. Implement proper access controls and IAM roles

try:
    # Use Application Default Credentials (ADC) for secure authentication
    # This works with Workload Identity Federation, service accounts, or local development
    storage_client = storage.Client()
    
    bucket_name = os.getenv("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME must be set in the environment.")
    
    bucket = storage_client.bucket(bucket_name)
    print("GCS connected successfully using secure authentication")
    
except Exception as e:
    print(f"Error initializing GCS: {e}")
    bucket = None

def upload_file(file, filename):
    if not bucket:
        return None, "GCS is not initialized."
    try:
        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        return blob.public_url, None
    except Exception as e:
        return None, str(e) 