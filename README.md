# EC2 Metadata Gatherer

A Python utility script that extracts system and network metadata from an AWS EC2 instance, saves it to a local report, and uploads the generated file to an Amazon S3 bucket.

## Features

* **Metadata Extraction:** Gathers key instance details including:
  * Instance ID
  * Public & Private IP Addresses
  * Security Groups
  * Operating System Information
  * Active Shell Users
* **Local Reporting:** Automatically formats the data and saves it locally as `metadata.txt`.
* **Cloud Storage:** Uploads the local report directly to a specified Amazon S3 URI.

## Prerequisites

Before running this script, ensure you have the following configured on your EC2 instance:

* **Python 3.x** installed.
* **AWS SDK for Python (Boto3)** installed. 
* **AWS Credentials:** The instance must have the appropriate IAM permissions (usually attached via an IAM Instance Profile) granting `s3:PutObject` access to the target S3 bucket.

### Installing Dependencies

You can install the required Python libraries using pip:

pip install boto3
