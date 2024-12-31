import sys
from engine.template_parser import load_templates_from_directory
from engine.scanner import Scanner
from engine.utils import print_results


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <target_url> [<templates_directory>]")
        sys.exit(1)

    target_url = sys.argv[1] 
    templates_dir = sys.argv[2] if len(sys.argv) > 2 else "templates/http"

    # Load the templates
    templates = load_templates_from_directory(templates_dir)
    # Create the scanner instance
    scanner = Scanner(templates)

    # Run the scan
    results = scanner.scan(target_url)
    for idx, result in enumerate(results):
        print(f"Result #{idx + 1}, result for {result['name']}: {result['matched']}")


if __name__ == "__main__":
    main()
