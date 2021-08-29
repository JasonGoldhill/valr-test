variable "gcp_credentials" {
  type        = string
  sensitive   = true
  description = "Google Cloud service account credentials"
}

variable "gcp_project_id" {
  type        = string
  sensitive   = false
  description = "Google Cloud project ID"
}

variable "gcp_region" {
  type        = string
  sensitive   = false
  description = "Google Cloud region"
}

variable "gke_num_nodes" {
  default     = 2
  description = "Number of gke nodes"
}