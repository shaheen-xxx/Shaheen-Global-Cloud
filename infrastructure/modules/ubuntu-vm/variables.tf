variable "server_name" {
  description = "Name of the server"
  type        = string
}

variable "region" {
  description = "Cloud provider region"
  type        = string
}

variable "server_size" {
  description = "Size/flavor of the server"
  type        = string
}

variable "os_image" {
  description = "Operating system image"
  type        = string
}

variable "user_data" {
  description = "cloud-init user data script"
  type        = string
  default     = ""
}

variable "provider_token" {
  description = "Provider API token"
  type        = string
  sensitive   = true
  default     = "mock-token"
}
