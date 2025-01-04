import logging
from updateutils import get_update_tool_callback
from pdcpauth import check_and_validate_credentials

# Define the banner
banner = '''
             __________________
  ____  ____/_  __/ ____/ ____/
 / __ \/ __ \/ / / __/ / /
/ /_/ / /_/ / / / /___/ /___
\____/ .___/_/ /_____/\____/
    /_/                          1.0.0
'''

# Show the banner to the user
def show_banner():
    print(f"{banner}")
    print("\t\toptec.example.com\n")

# Update nuclei binary/tool to the latest version
def nuclei_tool_update_callback():
    show_banner()
    get_update_tool_callback('nuclei', '1.0.0')()

# Authenticate with PDCP
def auth_with_pdcp():
    show_banner()
    check_and_validate_credentials('nuclei')

# Example usage
if __name__ == "__main__":
    auth_with_pdcp()
    nuclei_tool_update_callback()
