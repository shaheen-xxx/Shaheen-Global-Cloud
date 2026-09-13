terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "null" {}
provider "random" {}

resource "random_string" "server_id" {
  length  = 8
  special = false
  upper   = false
}

resource "random_integer" "ipv4" {
  min = 10
  max = 254
}

# Mock server resource - in production this would call actual cloud provider API
resource "null_resource" "ubuntu_server" {
  provisioners = {
    server_name = var.server_name
    region      = var.region
    size        = var.server_size
    image       = var.os_image
    user_data   = base64encode(var.user_data)
  }

  lifecycle {
    ignore_changes = all
  }
}

locals {
  server_config = {
    name        = var.server_name
    region      = var.region
    size        = var.server_size
    image       = var.os_image
    token       = var.provider_token
    server_id   = random_string.server_id.result
  }
}
