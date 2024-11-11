terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "totes-terraform-state"
    key = "de-project-bond-team/terraform.tfstate"
    region = "eu-west-2"
  }
}