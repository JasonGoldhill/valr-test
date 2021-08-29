resource "kubernetes_manifest" "deployment_api" {
  manifest = {
    "apiVersion" = "apps/v1"
    "kind"       = "Deployment"
    "metadata" = {
      "labels" = {
        "app" = "api"
      }
      "name" = "api"
    }
    "spec" = {
      "replicas" = 3
      "selector" = {
        "matchLabels" = {
          "app" = "api"
        }
      }
      "template" = {
        "metadata" = {
          "labels" = {
            "app" = "api"
          }
        }
        "spec" = {
          "containers" = [
            {
              "image"           = "gcr.io/valr-test/valr-test-image"
              "imagePullPolicy" = "Always"
              "name"            = "api"
              "ports" = [
                {
                  "containerPort" = 5000
                },
              ]
            },
          ]
        }
      }
    }
  }
}
