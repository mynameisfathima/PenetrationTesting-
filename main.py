import requests
import yaml

def load_yaml(file_path):
    """
    Load and parse a YAML file.

    Args:
        file_path (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        return None

def check_http_page(base_url, path, allow_redirects=True, max_redirects=1):
    """
    Sends a GET request to the given URL and checks if the response status code is 200.

    Args:
        base_url (str): The base URL to send the request to.
        path (str): The path to append to the base URL.
        allow_redirects (bool): Whether to allow redirects.
        max_redirects (int): Maximum number of redirects to follow.

    Returns:
        bool: True if the response status code is 200, False otherwise.
    """
    url = f"http://{base_url}{path}"
    try:
        response = requests.get(url, allow_redirects=allow_redirects, timeout=5)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error occurred while checking HTTP page: {e}")
        return False

if __name__ == "__main__":
    yaml_file_path = r"C:\Users\ASUS\kmea\PenetrationTesting\intake\test.yaml"
    config = load_yaml(yaml_file_path)

    if not config:
        print("Failed to load configuration from YAML file.")
        exit(1)

    base_url = "google.com"
    http_config = config.get('http', [])

    for entry in http_config:
        method = entry.get('method', 'GET')
        paths = entry.get('path', [])
        allow_redirects = entry.get('host-redirects', True)
        max_redirects = entry.get('max-redirects', 1)

        if method == 'GET':
            for path in paths:
                print(f"Checking HTTP page availability for {base_url}{path}...")
                is_available = check_http_page(base_url, path, allow_redirects, max_redirects)

                if is_available:
                    print(f"HTTP page at {base_url}{path} is available (status code 200).")
                    assert is_available, f"The page at {path} should be available."
                else:
                    print(f"HTTP page at {base_url}{path} is not available.")
                    assert is_available, f"The page at {path} is not available."
