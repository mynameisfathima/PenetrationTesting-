from typing import Dict, Any
from jinja2 import Template

def generate_html_report(data: Dict[str, Any], template_path: str = "scan_report.html"):
    # Load HTML template
    template = Template("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Website Scan Report</title>
    </head>
    <body>
        <h1>Website Scan Report</h1>
        <p><strong>Website:</strong> {{ website }}</p>
        <p><strong>Scan Date:</strong> {{ date }}</p>
        <h2>Summary</h2>
        <p>Total vulnerabilities found: {{ total_vulnerabilities }}</p>
        <h2>Vulnerability Details</h2>
        <table border="1">
            <thead>
                <tr>
                    <th>Vulnerability</th>
                    <th>Severity</th>
                    <th>Affected URL</th>
                    <th>Description</th>
                    <th>Recommendation</th>
                </tr>
            </thead>
            <tbody>
                {% for vuln in vulnerabilities %}
                <tr>
                    <td>{{ vuln.name }}</td>
                    <td>{{ vuln.severity }}</td>
                    <td>{{ vuln.url }}</td>
                    <td>{{ vuln.description }}</td>
                    <td>{{ vuln.recommendation }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """)

    # Render the template with data
    html_report = template.render(data)

    # Save the report to a file
    with open(template_path, "w") as file:
        file.write(html_report)

    print(f"Report generated successfully: {template_path}")
