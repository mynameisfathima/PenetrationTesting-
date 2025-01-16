import requests

class Scanner:
    def __init__(self, templates):
        self.templates = templates

    def scan(self, target_url):
        results = []

        try:
            response = requests.get(target_url, timeout=10)
        except requests.RequestException as e:
            print(f"Error fetching URL: {target_url} -> {e}")
            return []

        for template in self.templates:
            result = {
                "name": template.get("name", "Unnamed Template"),
                "matched": False,
                "severity": template.get("severity", "low"),
            }

            if "conditions" in template:
                for condition in template["conditions"]:
                    if condition.get("type") == "header":
                        header_name = condition.get("header")
                        header_value = condition.get("value")

                        # Check if header matches
                        if header_name in response.headers and response.headers[header_name] == header_value:
                            result["matched"] = True
                            break

            results.append(result)

        return results
import requests  # Alternative to a browser in real life
from typing import Dict, Any, List
from urllib.parse import urlparse
from .matchers import run_matchers

class Scanner:
    """
    The main scanning engine that takes Nuclei-like templates
    and a list of target URLs to test.
    """

    def __init__(self, templates: List[Dict[str, Any]]):
        self.templates = templates
        self.logged_urls = set()  # Set to track already logged URLs for warnings

    def scan(self, target_url: str):
        """
        Scan a single target URL with all loaded templates.
        """
        results = []
        # Ensure the target URL has a scheme (http:// or https://)
        target_url = self._ensure_url_scheme(target_url)

        for template in self.templates:
            template_id = template.get("id", "unknown-id")
            template_info = template.get("info", {})

            for key, value in template.items():
                if key == "id" or key == "info":
                    continue
                elif key == "http":
                    template_requests = template.get("http", [])
                    for request_config in template_requests:
                        result = self._process_http_request(template_id, template_info, request_config, target_url)
                        if result:
                            results.append(result)
                elif key == "ssl":
                    template_requests = template.get("ssl", [])
                    for request_config in template_requests:  # SSL requests
                        result = self._process_ssl_request(template_id, template_info, request_config, target_url)
                        if result:
                            results.append(result)

        return results

    def _ensure_url_scheme(self, target_url: str) -> str:
        """
        Ensure that the URL has a scheme (http:// or https://).
        If no scheme is provided, default to http://.
        """
        parsed_url = urlparse(target_url)
        if not parsed_url.scheme:
            target_url = f"http://{target_url}"
        return target_url

    def _process_ssl_request(self, template_id, template_info, request_config, target_url):
        paths = request_config.get("path", [])
        matchers_config = request_config.get("matchers", [])
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")
            try:
                response = requests.get(url, verify=True, timeout=10)
                if response.url.startswith("https://"):
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": False,  # Negative result
                    }
                else:
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": True,  # Positive result
                    }
            except requests.exceptions.SSLError:
                return {
                    "template_id": template_id,
                    "name": template_info.get("name"),
                    "author": template_info.get("author"),
                    "severity": template_info.get("severity"),
                    "url": url,
                    "status_code": "N/A",
                    "matched": True,  # Positive result for SSL error
                }
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] The request for SSL failed: {e}")
                return None

    def _process_http_request(self, template_id, template_info, request_config, target_url):
        """
        Process a single request configuration from a template.
        """
        method = request_config.get("method", "GET").upper()
        paths = request_config.get("path", [])
        matchers_config = request_config.get("matchers", [])
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")  # Clean extra slashes
            
            try:
                # Make the request based on method
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, timeout=5)

                # Evaluate matchers
                matched_result = run_matchers(response, matchers_config)

                # Combine results: Header issues override matchers
                if matched_result:  # For clarity, 'True' means a vulnerability
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": True,
                    }
                else:
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": False,
                    }

            except requests.RequestException as e:
                print(f"[ERROR] Request failed for {url}: {e}")
                return None
        return None
