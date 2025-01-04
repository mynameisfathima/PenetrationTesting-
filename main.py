import argparse
import os
import yaml
from engine.template_parser import load_templates_from_directory
from engine.scanner import Scanner
from banner import show_banner  # Assuming you have the banner function
from urllib.parse import urlparse


def main():
    # Show banner at the start
    show_banner()

    parser = argparse.ArgumentParser(
        description="A tool for scanning a target URL using templates."
    )

    # Add target_url argument (no default, making it required)
    parser.add_argument(
        "target_url",
        help="The target URL to scan.",
    )

    parser.add_argument(
        "-t", "--templates",
        default="templates/",
        help=("Path to a specific template file or directory containing YAML templates. "
              "Default: templates/"),
    )

    # Parse arguments
    args = parser.parse_args()

    # Define target_url from the command line argument
    target_url = args.target_url  # Get the target URL from the argument

    # Check if the target_url has a scheme (http:// or https://)
    parsed_url = urlparse(target_url)
    if not parsed_url.scheme:
        # If no scheme, prepend http://
        target_url = f"http://{target_url}"

    templates_path = args.templates

    # Check and load YAML templates
    if os.path.isfile(templates_path) and templates_path.endswith(".yaml"):
        print(f"Loading specific template: {templates_path}")
        with open(templates_path, "r") as file:
            try:
                templates = [yaml.safe_load(file)]  # Parse the YAML into a dictionary
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
                exit(1)
    elif os.path.isdir(templates_path):
        print(f"Loading all YAML files from directory: {templates_path}")
        templates = load_templates_from_directory(templates_path)
    else:
        print(f"Invalid path: {templates_path}. Ensure it points to a .yaml file or a directory.")
        exit(1)

    # Ask the user if they want to scan all or specific templates
    choice = input("Do you want to scan ALL templates or SPECIFIC ones? (Y/N): ").strip().lower()

    if choice == 'y':
        # Scan all templates
        print("Scanning all templates...")
        selected_templates = templates
    elif choice == 'n':
        # Let the user select specific templates by numbers
        print("\nPlease enter the numbers of the templates you'd like to scan (e.g., 1 2 4 6): ")
        # Safe print for template names
        for idx, template in enumerate(templates, 1):
            # Ensure the template has the expected structure before accessing it
            template_name = template.get('info', {}).get('name', 'Unnamed Template')
            print(f"{idx}. {template_name}")  # Display template names for selection
        
        selected_numbers = input("\nEnter your choices: ").strip().split()
        selected_templates = []

        # Add the selected templates to the list
        try:
            selected_numbers = [int(num) - 1 for num in selected_numbers]  # Convert to 0-based index
            selected_templates = [templates[i] for i in selected_numbers]
        except (ValueError, IndexError):
            print("Invalid input. Exiting.")
            exit(1)

    else:
        print("Invalid choice. Exiting.")
        exit(1)

    # Create the scanner instance
    scanner = Scanner(selected_templates)

    # Run the scan
    print(f"\nScanning target URL: {target_url}")
    results = scanner.scan(target_url)

    # Display the results
    print("\nScan Results:")
    if not results:
        print("No results found or templates did not match any conditions.")
    else:
        for idx, result in enumerate(results):
            print(f"[{idx + 1}] {result['name']}:[{result['matched']}][{result['severity']}]")

if __name__ == "__main__":
    main()
