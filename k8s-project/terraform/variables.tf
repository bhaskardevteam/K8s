variable "project_name" {
  type    = string
  default = "k8sdemo"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "aks_node_count" {
  type    = number
  default = 3
}

variable "aks_vm_size" {
  type    = string
  default = "Standard_D2s_v5"
}
