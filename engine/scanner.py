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
        self.logged_urls = set()  # Set to track already logged URLs for warnings

    def scan(self, target_url: str):
        """
        Scan a single target URL with all loaded templates.
        """
        results = []
        for template in self.templates:
            template_id = template.get("id", "unknown-id")
            template_info = template.get("info", {})
            template_requests = template.get("http", [])

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

        for path in paths:
            url = path.replace("{{BaseURL}}", target_url).strip("/")  # Remove extra slashes

            try:
                # Make the request based on method
                if method == "GET":
                    response = requests.get(url, timeout=5)
                elif method == "POST":
                    response = requests.post(url, timeout=5)
                else:
                    response = requests.request(method, url, timeout=5)

                # Perform header checks and warnings
                header_warnings = self._check_headers(response.headers, url)
                if header_warnings:
                    for warning in header_warnings:
                        print(f"[WARNING] Header issues found for {url}: {warning}")

                # Check if any critical headers are missing and set matched to False
                if any("Missing" in warning for warning in header_warnings):
                    return {
                        "template_id": template_id,
                        "name": template_info.get("name"),
                        "author": template_info.get("author"),
                        "severity": template_info.get("severity"),
                        "url": url,
                        "status_code": response.status_code,
                        "matched": False,  # Matched is False due to missing headers
                    }

                # Check matchers and handle result
                matched_result = run_matchers(response, matchers_config)

                # Only consider the result if no header issues are found and matchers are true
                if matched_result and not header_warnings:
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

        return None
    def _check_headers(self, headers: Dict[str, str], url: str) -> List[str]:
        """
        Analyzes headers for missing or insecure configurations.

        Args:
            headers (Dict[str, str]): The HTTP response headers.

        Returns:
            List[str]: A list of warnings about header issues.
        """
        warnings = []

        # If the URL has already been logged, don't repeat the warnings
        if url in self.logged_urls:
            return warnings
        self.logged_urls.add(url)

        # Define header checks as a list of tuples: (header name, check function)
        header_checks = [
            ("Content-Security-Policy", self._check_csp),
            ("X-Frame-Options", self._check_x_frame),
            ("Strict-Transport-Security", self._check_hsts),
        ]

        # Perform each check and collect warnings
        for header_name, check_func in header_checks:
            warning = check_func(headers)
            if warning:
                warnings.append(warning)

        return warnings

    def _check_csp(self, headers: Dict[str, str]) -> str:
        """
        Check Content-Security-Policy header for issues.

        Args:
            headers (Dict[str, str]): The HTTP response headers.

        Returns:
            str: A warning message if issues found, otherwise empty string.
        """
        if "Content-Security-Policy" not in headers:
            return "Missing Content-Security-Policy header."
        elif "unsafe-inline" in headers["Content-Security-Policy"]:
            return "CSP uses 'unsafe-inline', which is insecure."
        return ""  # No issues with CSP header

    def _check_x_frame(self, headers: Dict[str, str]) -> str:
        """
        Check X-Frame-Options header for issues.

        Args:
            headers (Dict[str, str]): The HTTP response headers.

        Returns:
            str: A warning message if issues found, otherwise empty string.
        """
        if "X-Frame-Options" not in headers:
            return "Missing X-Frame-Options header."
        elif headers["X-Frame-Options"].lower() not in ["deny", "sameorigin"]:
            return f"Insecure X-Frame-Options value: {headers['X-Frame-Options']}"
        return ""  # No issues with X-Frame-Options header

    def _check_hsts(self, headers: Dict[str, str]) -> str:
        """
        Check Strict-Transport-Security (HSTS) header for issues.

        Args:
            headers (Dict[str, str]): The HTTP response headers.

        Returns:
            str: A warning message if issues found, otherwise empty string.
        """
        if "Strict-Transport-Security" not in headers:
            return "Missing Strict-Transport-Security header (HSTS)."
        return ""  # No issues with HSTS header
