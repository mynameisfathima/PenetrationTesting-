import os
import yaml
from typing import List, Dict, Any


def load_templates_from_directory(directory: str) -> List[Dict[str, Any]]:
    """
    Loads all YAML files from the specified directory and returns
    them as a list of parsed dictionaries.

    The directory needs to be till yaml or else nothing at all 
    incase of no  directory is passed, load all yaml 
    TODO: Handled by another function - Who will take care of this ?
    """
    templates = []
    for filename in os.listdir(directory):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    data = yaml.safe_load(f) # Using safe load here, I dont want deserialization attack happening here !
                    if data:
                        templates.append(data) # TODO : Handle else case YAML errors may need a blank
                except yaml.YAMLError as e:
                    print(f"[ERROR] Failed to parse YAML file {filename}: {e}")
    return templates
