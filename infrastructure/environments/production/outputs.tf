output "server_id" {
  description = "ID of the created server"
  value       = module.ubuntu_vm.server_id
}

output "server_name" {
  description = "Name of the server"
  value       = module.ubuntu_vm.server_name
}

output "ipv4" {
  description = "IPv4 address of the server"
  value       = module.ubuntu_vm.ipv4
}

output "ipv6" {
  description = "IPv6 address of the server"
  value       = module.ubuntu_vm.ipv6
}
