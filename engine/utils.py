import json
from typing import List, Dict, Any


def print_results(results: List[Dict[str, Any]]):
    """
    Print or store the results of the scanning in a desired format.
    Here, we do a simple JSON dump to console.
    """
    for res in results:
        print(json.dumps(res, indent=2))
