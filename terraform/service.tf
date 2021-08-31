resource "kubernetes_manifest" "service_api_service" {
  depends_on = [
    google_container_cluster.primary
  ]
  manifest = {
    "apiVersion" = "v1"
    "kind"       = "Service"
    "metadata" = {
      "name" = "api-service"
    }
    "spec" = {
      "ports" = [
        {
          "port"       = 5000
          "protocol"   = "TCP"
          "targetPort" = 5000
        },
      ]
      "selector" = {
        "app" = "api"
      }
      "type" = "LoadBalancer"
    }
  }
}
