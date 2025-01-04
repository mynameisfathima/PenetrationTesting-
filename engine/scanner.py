# engine/scanner.py
class Scanner:
    def __init__(self, templates):
        """
        Initializes the Scanner with a list of templates.
        Args:
            templates (list): A list of templates to use for scanning.
        """
        self.templates = templates

    def scan(self, target_url):
        """
        Scans the target URL using the provided templates.
        Args:
            target_url (str): The target URL to scan.
        Returns:
            list: A list of results from the scan.
        """
        results = []
        for template in self.templates:
            matched = self._match_template(template, target_url)
            # Collect the result for this template
            results.append({
                "name": template.get("name", "Unnamed Template"),
                "matched": matched,
                "severity": template.get("severity", "low"),
            })
        return results

    def _match_template(self, template, target_url):
        """
        Placeholder method for matching a template to a target URL.
        You can extend this method with custom logic to check patterns or conditions.
        Args:
            template (dict): A single template (dict) to match.
            target_url (str): The target URL.
        Returns:
            bool: Whether the target URL matches the template.
        """
        # Basic matching logic (you can extend it as needed)
        return "example" in target_url  # Example condition for matching
