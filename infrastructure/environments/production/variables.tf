variable "provider_api_token" {
  description = "API token for cloud provider"
  type        = string
  sensitive   = true
  default     = "mock-token-for-testing"
}

variable "region" {
  description = "Cloud provider region"
  type        = string
  default     = "fsn1"
}

variable "server_name" {
  description = "Name of the server"
  type        = string
}

variable "server_size" {
  description = "Size/flavor of the server"
  type        = string
  default     = "cx22"
}

variable "os_image" {
  description = "Operating system image"
  type        = string
  default     = "ubuntu-24.04"
}

variable "user_data" {
  description = "cloud-init user data script"
  type        = string
  default     = ""
}
