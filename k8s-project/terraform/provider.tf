terraform {
  required_version = ">= 1.6.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.100"
    }
  }
  # In real use, configure a remote backend (Azure Storage) so state
  # is shared and locked across the team, instead of local state:
  # backend "azurerm" {}
}

provider "azurerm" {
  features {}
}
