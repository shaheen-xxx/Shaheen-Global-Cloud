module "ubuntu_vm" {
  source = "../../modules/ubuntu-vm"

  server_name      = var.server_name
  region           = var.region
  server_size      = var.server_size
  os_image         = var.os_image
  user_data        = var.user_data
  provider_token   = var.provider_api_token
}
