import logging
from updateutils import get_update_tool_callback
from auth.pdcpauth import check_and_validate_credentials
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define the banner with red color for ASCII art
banner = f'''
{Fore.RED}             __________________
{Fore.RED}  ____  ____/{Fore.RED}_  __/ ____/ ____/
{Fore.RED} / __ \\/ __ \\/ / / __/ / /
{Fore.RED}/ /_/ / /_/ / / / /___/ /___
{Fore.RED}\\____/ .___/_/ /_____/\\____/
{Fore.RED}    /_/                        {Fore.YELLOW}1.0.0{Style.RESET_ALL}

{Style.BRIGHT}{Fore.GREEN}                optec.asfaad.com
'''

# Show the banner to the user
def show_banner():
    print(banner)

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
