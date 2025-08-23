terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  description = "The Azure region to deploy resources"
  type        = string
  default     = "East US"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "loy-dev-rg"
}

variable "storage_account_name" {
  description = "The name of the storage account"
  type        = string
  default     = "loydevstorage"
}

variable "tags" {
  description = "Tags to be applied to resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Owner       = "Loyalty"
    CostCenter  = "CC-2025-018"
    Compliance  = "PCI"
    Application = "Loyalty Platform"
  }
}

resource "azurerm_resource_group" "loyalty" {
  name     = var.resource_group_name
  location = var.location

  tags = var.tags
}

resource "azurerm_storage_account" "loyalty" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.loyalty.name
  location                 = azurerm_resource_group.loyalty.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = var.tags
}

resource "azurerm_virtual_network" "loyalty" {
  name                = "loy-dev-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.loyalty.location
  resource_group_name = azurerm_resource_group.loyalty.name

  tags = var.tags
}

resource "azurerm_subnet" "loyalty" {
  name                 = "loy-dev-subnet"
  resource_group_name  = azurerm_resource_group.loyalty.name
  virtual_network_name = azurerm_virtual_network.loyalty.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_private_endpoint" "loyalty" {
  name                = "loy-dev-pe"
  location            = azurerm_resource_group.loyalty.location
  resource_group_name = azurerm_resource_group.loyalty.name
  subnet_id           = azurerm_subnet.loyalty.id

  private_service_connection {
    name                           = "loy-dev-psc"
    private_connection_resource_id = azurerm_storage_account.loyalty.id
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }

  tags = var.tags
}

resource "azurerm_network_security_group" "loyalty" {
  name                = "loy-dev-nsg"
  location            = azurerm_resource_group.loyalty.location
  resource_group_name = azurerm_resource_group.loyalty.name

  security_rule {
    name                       = "AllowHttpsInBound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }

  tags = var.tags
}

resource "azurerm_subnet_network_security_group_association" "loyalty" {
  subnet_id                 = azurerm_subnet.loyalty.id
  network_security_group_id = azurerm_network_security_group.loyalty.id
}

output "resource_group_id" {
  description = "The ID of the resource group"
  value       = azurerm_resource_group.loyalty.id
}

output "storage_account_id" {
  description = "The ID of the storage account"
  value       = azurerm_storage_account.loyalty.id
}

output "private_endpoint_id" {
  description = "The ID of the private endpoint"
  value       = azurerm_private_endpoint.loyalty.id
}