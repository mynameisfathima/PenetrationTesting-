import requests  # Alternative to a browser in real lyf
from typing import Dict, Any, List
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
        for template in self.templates:
            template_id = template.get("id", "unknown-id")
            template_info = template.get("info", {})
            for key, value in template.items():
                if key == "id":
                    continue
                elif key == "info":
                    continue
                elif key == "http":
                    template_requests = template.get("http", [])
                    for request_config in template_requests:
                        result = self._process_http_request(template_id, template_info, request_config, target_url)
                        if result:
                            results.append(result)
                elif key == "ssl":
                    template_requests = template.get("ssl", [])
                    for request_config in template_requests: # SSL
                        results = self._process_ssl_request(template_id, template_info, request_config, target_url)
        return results

    def _process_ssl_request(self, template_id, template_info, request_config, target_url):
        paths = request_config.get("path", []) # TODO : Strip this to just domain name in case any path exists 
        matchers_config = request_config.get("matchers", [])
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")
            try:
                response = requests.get(url, verify=True)
                if response.url.startswith("https://"):
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "Flase", # As a postive result
                    }
                else:
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "True", # As a negetive result
                    }
            except requests.exceptions.SSLError:
                return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "True", # As a negetive result
                    }
            except requests.exceptions.RequestException as e:
                print("The request was errored out ", str(e))


    def _process_http_request(self, template_id, template_info, request_config, target_url):
        """
        Process a single request configuration from a template.
        """
        method = request_config.get("method", "GET").upper()
        paths = request_config.get("path", [])
        matchers_config = request_config.get("matchers", [])
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")  # Remove extra slashes # TODO : Check for slashes and/or double slashes and then remove the same #noqa
            
            try:
                # Make the request based on method
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, timeout=5)

                # Evaluate matchers
                matched_result = run_matchers(response, matchers_config)

                # Combine results: Header issues override matchers
                if matched_result: # For clarity Lets keep if true it means there is a vulnerability and false means all good
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "True",
                    }
                else:
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": "False",
                    }

            except requests.RequestException as e:
                print(f"[ERROR] Request failed for {url}: {e}")

        return None

  
