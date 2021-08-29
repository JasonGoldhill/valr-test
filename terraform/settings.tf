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
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.4.1"
    }
  }

  required_version = "1.0.5"
}

provider "google" {
  project     = var.gcp_project_id
  credentials = var.gcp_credentials
  region      = var.gcp_region
}

data "google_client_config" "default" {}
data "google_container_cluster" "my_cluster" {
  name     = "${var.gcp_project_id}-gke"
  location = var.gcp_region
  depends_on = [
    google_container_cluster.primary,
  ]
}

provider "kubernetes" {
  host                   = "https://${data.google_container_cluster.my_cluster.endpoint}"
  token                  = data.google_client_config.default.access_token
  cluster_ca_certificate = base64decode(data.google_container_cluster.my_cluster.master_auth[0].cluster_ca_certificate)
  experiments {
    manifest_resource = true
  }
}
