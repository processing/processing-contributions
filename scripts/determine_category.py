"""
Reads issue labels from a JSON string and determines the category of the issue.
"""

import json
import sys

valid_categories = ["examples", "mode", "tool", "library"]

def determine_category(labels_json):
    labels = json.loads(labels_json)
    found_categories = [label for label in labels if label in valid_categories]

    if len(found_categories) == 1:
        return found_categories[0]
    elif len(found_categories) > 1:
        raise ValueError(f"Multiple valid categories found: ({', '.join(found_categories)}). Please ensure only one valid label is applied.")
    else:
        return None

if __name__ == "__main__":
    labels_json = sys.argv[1]
    try:
        category = determine_category(labels_json)
        if category:
            print(f"category={category}")
        else:
            print(f"Category is empty. Please ensure the issue has a valid label (options: {', '.join(valid_categories)}).")
            sys.exit(1)
    except ValueError as e:
        print(str(e))
        sys.exit(1)
