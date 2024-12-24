import requests
from typing import Dict, Any, List
from .matchers import run_matchers


class Scanner:
    """
    The main scanning engine that takes Nuclei-like templates
    and a list of target URLs to test.
    """

    def __init__(self, templates: List[Dict[str, Any]]):
        self.templates = templates

    def scan(self, target_url: str):
        """
        Scan a single target URL with all loaded templates.
        """
        results = []
        for template in self.templates:
            template_id = template.get("id", "unknown-id")
            template_info = template.get("info", {})
            template_requests = template.get("http", [])  # TODO : Add more protocols, maybe make them into class
            for request_config in template_requests:
                result = self._process_request(template_id, template_info, request_config, target_url)
                if result:
                    results.append(result)

        return results

    def _process_request(self, template_id, template_info, request_config, target_url):
        """
        Process a single request configuration from a template.
        """
        method = request_config.get("method", "GET").upper()
        paths = request_config.get("path", [])
        matchers_config = request_config.get("matchers", [])

        # For each path in the template, we replace {{BaseURL}} with the target_url
        for path in paths:
            url = path.replace("{{BaseURL}}", target_url)

            try:
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, timeout=5)
                else:
                    # Extend this as necessary
                    response = requests.request(method, url, timeout=5)

                if run_matchers(response, matchers_config):
                    # If all matchers pass, we consider it a "hit"
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": True,
                    }

            except requests.RequestException as e:
                print(f"[ERROR] Request failed for {url}: {e}")

        # If no match or an error, return None
        return None
