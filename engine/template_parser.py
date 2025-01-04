import os
import yaml

# Function to load templates from the specified directory (including subdirectories)
def load_templates_from_directory(directory):
    templates = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    try:
                        templates.append(yaml.safe_load(f))  # Load and append the YAML template
                    except yaml.YAMLError as e:
                        print(f"Error parsing YAML file: {file_path} -> {e}")
    return templates
