resource "google_container_cluster" "primary" {
  name               = "${var.gcp_project_id}-gke"
  location           = var.gcp_region
  initial_node_count = var.gke_num_nodes

  # network    = google_compute_network.vpc.name
  # subnetwork = google_compute_subnetwork.subnet.name
  node_config {
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
    machine_type = "n1-standard-1"
    labels = {
      env = var.gcp_project_id
    }
    tags = ["gke-node", "${var.gcp_project_id}-gke"]
  }
  timeouts {
    create = "30m"
    update = "40m"
  }
  ip_allocation_policy {
    cluster_ipv4_cidr_block       = "10.92.0.0/14"
    cluster_secondary_range_name  = "gke-${var.gcp_project_id}-gke-pods-09f3092d"
    services_ipv4_cidr_block      = "10.96.0.0/20"
    services_secondary_range_name = "gke-${var.gcp_project_id}-gke-services-09f3092d"
  }
}
