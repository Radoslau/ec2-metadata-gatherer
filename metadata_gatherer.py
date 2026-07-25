import urllib.request
import urllib.error

def get_imds_token():
    try:
        req = urllib.request.Request(
            "http://169.254.169.254/latest/api/token",
            method="PUT",
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def get_aws_metadata(path, token):
    if not token:
        return "N/A (Token missing)"
    try:
        url = f"http://169.254.169.254/latest/meta-data/{path}"
        req = urllib.request.Request(url, headers={"X-aws-ec2-metadata-token": token})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "None"
        return f"HTTP Error: {e.code}"
    except Exception as e:
        return f"Error: {str(e)}"

def get_os_info():
    try:
        with open('/etc/os-release', 'r') as f:
            os_data = {}
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    os_data[key] = value.strip('"')
            return os_data.get('PRETTY_NAME', os_data.get('NAME', 'Unknown OS'))
    except FileNotFoundError:
        return "OS info not found"

def get_shell_users():
    valid_users = []
    try:
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 7:
                    username = parts[0]
                    shell = parts[-1]
                    if shell in ['/bin/bash', '/bin/sh']:
                        valid_users.append(username)
        return valid_users
    except FileNotFoundError:
        return ["Error reading /etc/passwd"]
