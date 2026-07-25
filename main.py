from metadata_gatherer import get_imds_token, get_aws_metadata, get_os_info, get_shell_users

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
    filename = "ec2_metadata.txt"
    with open(filename, "w") as file:
        file.write(report)

    print(f"Data successfully written: {filename}")
    return filename

if __name__ == "__main__":
    generate_report()
