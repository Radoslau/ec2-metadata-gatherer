from metadata_gatherer import get_imds_token, get_aws_metadata, get_os_info, get_shell_users
from urllib.parse import urlparse
import boto3

def upload_to_s3(file_path, s3_uri):
    """Uploads a local file to an S3 bucket using an S3 URI."""
    try:
        # Parse the s3 URI
        parsed_uri = urlparse(s3_uri)
        bucket_name = parsed_uri.netloc
        prefix = parsed_uri.path.lstrip('/')
        
        # Construct object key
        if prefix.endswith('/') or not prefix:
            object_name = f"{prefix}{file_path}"
        else:
            object_name = f"{prefix}/{file_path}"
            
        print(f"Uploading {file_path} to bucket '{bucket_name}'...")
        
        s3_client = boto3.client('s3')
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"Successfully uploaded to S3://{bucket_name}/{object_name}")
        
    except Exception as e:
        print(f"Failed to upload to S3: {e}")

def generate_report():
    print("Gathering EC2 instance metadata")

    # Fetching data here
    token = get_imds_token()
    instance_id = get_aws_metadata("instance-id", token)
    public_ip = get_aws_metadata("public-ipv4", token)
    private_ip = get_aws_metadata("local-ipv4", token)

    sg_raw = get_aws_metadata("security-groups", token)
    security_groups = sg_raw.splitlines() if "Error" not in sg_raw else [sg_raw]

    # Fetchig OS data 
    os_info = get_os_info()
    users = get_shell_users()

    # Proper output
    report = (
        f"--- EC2 Instance Metadata Report ---\n"
        f"Instance ID    : {instance_id}\n"
        f"Public IP      : {public_ip}\n"
        f"Private IP     : {private_ip}\n"
        f"Security Groups: {', '.join(security_groups)}\n"
        f"Operating Sys  : {os_info}\n"
        f"Shell Users    : {', '.join(users)}\n"
        f"------------------------------------\n"
    )

    # File handler
    filename = "metadata.txt"
    with open(filename, "w") as file:
        file.write(report)

    print(f"Data successfully written: {filename}")
    return filename
# Local report
if __name__ == "__main__":
    report_file = generate_report()

    # S3 Upload proceeds here

    TARGET_S3_URI = "s3://applicant-task/instance-143/"
    upload_to_s3(report_file, TARGET_S3_URI)


