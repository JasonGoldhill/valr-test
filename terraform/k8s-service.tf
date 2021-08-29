resource "kubernetes_manifest" "service_api" {
  manifest = {
    "apiVersion" = "v1"
    "kind"       = "Service"
    "metadata" = {
      "name" = "api"
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
