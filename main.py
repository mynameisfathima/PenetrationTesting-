import argparse
import os
import yaml
from engine.template_parser import load_templates_from_directory
from engine.scanner import Scanner
from banner import show_banner  # Assuming you have the banner function

def load_templates_from_directory_recursive(directory_path):
    """
    Recursively loads all YAML files from a directory and its subdirectories.
    """
    templates = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as file:
                    try:
                        templates.append(yaml.safe_load(file))  # Parse the YAML file
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file {file_path}: {e}")
    return templates

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

    # Add templates argument with default to 'templates/'
    parser.add_argument(
        "-t", "--templates",
        default="templates/http",  # Default is the 'templates/http' folder
        help=("Path to a specific template file or directory containing YAML templates. "
              "Default: templates/http")
    )

    # Parse arguments
    args = parser.parse_args()

    target_url = args.target_url  # Get the target URL from the argument
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
        print(f"Loading all YAML files from directory: {templates_path} (including subdirectories)")
        templates = load_templates_from_directory_recursive(templates_path)
    else:
        print(f"Invalid path: {templates_path}. Ensure it points to a .yaml file or a directory.")
        exit(1)

    # Create the scanner instance
    scanner = Scanner(templates)

    # Run the scan
    print(f"Scanning target URL: {target_url}")
    results = scanner.scan(target_url)

    # Display the results
    for idx, result in enumerate(results):
        print(f"[{idx + 1}] {result['name']}:[{result['matched']}][{result['severity']}]")

if __name__ == "__main__":
    main()
