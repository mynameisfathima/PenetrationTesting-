# main.py
import argparse
import os
import yaml
from engine.template_parser import load_templates_from_directory
from engine.scanner import Scanner
from banner import show_banner  # Assuming you have the banner function

def main():
    # Show banner at the start
    show_banner()

    # Remove target_url argument from command line input
    target_url = "http://www.google.com"  # Hardcode the target URL here

    parser = argparse.ArgumentParser(
        description="A tool for scanning a target URL using templates."
    )

    parser.add_argument(
    "-t", "--templates",
    default="templates/",
    help=("Path to a specific template file or directory containing YAML templates. "
          "Default: templates/"
        ),
    )
    
    

    # Parse arguments
    args = parser.parse_args()

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

