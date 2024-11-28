# DE-final-project-bond-team

## Table of Contents

- [About](#about)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Terraform](#terraform)
- [GitHub Actions](#github-actions)
- [Contact](#contact)

## About

This Data Engineering Project demonstrates the integration of multiple technologies and techniques to design and build a robust data pipeline, using best practices in Python programming, SQL, database modeling and could-based infrastructure. The primary objective is to create a reliable platform that extracts data from a simulated operational database, processes and archives it in structured formats within an AWS-based data lake, and remodels it into a data warehouse for analytical purposes.

## Features
- Automating data ingestion from a source database into S3 buckets.
- Transforming raw data into a star schema for storage in a data warehouse.
- Ensuring fault-tolerant operations with logging, monitoring, and alert systems.
- Maintaining data integrity with immutable storage in S3 and comprehensive historical records in the warehouse.
- Supporting business intelligence (BI) through real-time data visualizations.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Terraform installed
- PostgreSQL
- AWS account with configured permissions
- Locally stored AWS access and secret key
- Access to your database storing raw data
- S3 buckets for:
  - Ingestion: `s3://<bucket-name>/ingestion/`
  - Processed data: `s3://<bucket-name>/processed/`
- Change the email address for "aws_sns_topic_subscription" "email_notifications_target" located in terraform/monitoring.tf

### Installation

- Fork and clone the repo
- Create your virtual environment
- Install dependencies with pip install -r requirements.txt
- Configure AWS CLI if needed
- To enable running of tests using the test database use the make all command in the terminal
- Initialise terraform with terraform init in the terminal

## Usage

All deployment is handled by terraform with the pipeline starting its extraction run from the database containing the raw data on deployment, then running automatically 20 minutes after that.

## Terraform

- terraform init
- terraform plan
- terraform apply

To destroy
- terraform destroy

## Github Actions

The project uses GitHub Actions for CI/CD. The workflows are defined in the .github/workflows directory.



## Contact

dascrew | ieuanapwilliams@gmail.com
tischena | tischenko.anastasiia@lll.kpi.ua
bengriffiths95 | bengriffiths95@gmail.com
odashka | darya.babicheva@gmail.com
