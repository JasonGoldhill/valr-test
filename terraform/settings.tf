terraform {
  backend "remote" {
    organization = "jason-goldhill"

    workspaces {
      name = "valr-test"
    }
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.52.0"
    }
  }
}

provider "google" {
  project     = var.gcp_project_id
  credentials = var.gcp_credentials
  region      = var.gcp_region
}
