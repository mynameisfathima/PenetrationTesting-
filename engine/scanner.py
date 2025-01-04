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
