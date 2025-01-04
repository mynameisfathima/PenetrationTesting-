# engine/template_parser.py
import yaml
import os

def load_templates_from_directory(directory):
    """
    Loads all YAML templates from the specified directory.
    Args:
        directory (str): Path to the directory containing YAML template files.
    Returns:
        list: A list of parsed templates (as dictionaries).
    """
    templates = []
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".yaml"):  # Only load .yaml files
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                try:
                    # Parse the YAML file into a dictionary and append to templates list
                    templates.append(yaml.safe_load(file))
                except yaml.YAMLError as e:
                    print(f"Error parsing YAML file {filename}: {e}")
    return templates
