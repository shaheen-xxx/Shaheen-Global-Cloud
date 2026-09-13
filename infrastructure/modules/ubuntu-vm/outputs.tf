output "server_id" {
  description = "ID of the server"
  value       = "mock-server-${random_string.server_id.result}"
}

output "server_name" {
  description = "Name of the server"
  value       = var.server_name
}

output "ipv4" {
  description = "IPv4 address"
  value       = "192.168.1.${random_integer.ipv4.result}"
}

output "ipv6" {
  description = "IPv6 address"
  value       = "2001:db8::${random_integer.ipv4.result}"
}
