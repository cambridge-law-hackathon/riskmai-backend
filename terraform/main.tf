# Configure the Google Cloud Provider
terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

# Enable required APIs
resource "google_project_service" "required_apis" {
  for_each = toset([
    "firestore.googleapis.com",
    "storage.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ])
  
  service = each.value
  disable_dependent_services = true
}

# Create Google Cloud Storage bucket
resource "google_storage_bucket" "business_risk_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true  # For development - remove in production

  # Enable versioning for data protection
  versioning {
    enabled = true
  }

  # Configure lifecycle rules
  lifecycle_rule {
    condition {
      age = 365  # Keep files for 1 year
    }
    action {
      type = "Delete"
    }
  }

  # Configure uniform bucket-level access
  uniform_bucket_level_access = true

  # Add labels for better organization
  labels = {
    environment = var.environment
    project     = "business-risk"
  }
}

# Create IAM binding for the bucket (using current user)
resource "google_storage_bucket_iam_binding" "bucket_iam" {
  bucket = google_storage_bucket.business_risk_bucket.name
  role   = "roles/storage.objectAdmin"
  members = [
    "user:${data.google_client_openid_userinfo.current_user.email}"
  ]
}

# Get current user info for IAM bindings
data "google_client_openid_userinfo" "current_user" {}

# Create Firestore database
resource "google_firestore_database" "business_risk_firestore" {
  name        = "business-risk-db"
  location_id = var.region
  type        = "FIRESTORE_NATIVE"

  depends_on = [google_project_service.required_apis]
}

# Grant necessary roles to current user
resource "google_project_iam_member" "firestore_user" {
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "user:${data.google_client_openid_userinfo.current_user.email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "user:${data.google_client_openid_userinfo.current_user.email}"
}

# Output important information
output "bucket_name" {
  description = "Name of the created GCS bucket"
  value       = google_storage_bucket.business_risk_bucket.name
}

output "firebase_project_id" {
  description = "Firebase project ID (same as GCP project ID)"
  value       = var.project_id
}

output "current_user_email" {
  description = "Email of the authenticated user"
  value       = data.google_client_openid_userinfo.current_user.email
} 