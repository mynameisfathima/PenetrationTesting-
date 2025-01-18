from jinja2 import Template
import datetime

# Sample scan data
data = {
    "website": "http://example.com",
    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_vulnerabilities": 2,
    "vulnerabilities": [
        {
            "type": "SQL Injection",
            "severity": "High",
            "url": "http://example.com/login",
            "description": "SQL injection vulnerability in login form.",
            "recommendation": "Sanitize user inputs using prepared statements."
        },
        {
            "type": "XSS",
            "severity": "Medium",
            "url": "http://example.com/search",
            "description": "Reflected XSS vulnerability in the search bar.",
            "recommendation": "Escape special characters in user input."
        }
    ]
}

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
                <td>{{ vuln.type }}</td>
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
with open("scan_report.html", "w") as file:
    file.write(html_report)

print("Report generated successfully: scan-report.html")
