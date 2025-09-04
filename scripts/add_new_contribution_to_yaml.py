"""
given properties, add a new contribution to the contributions.yaml database file.
"""
from datetime import datetime, UTC
import json
import pathlib
from sys import argv

from ruamel.yaml import YAML


def split_categories(categories):
    categories = sorted(categories.replace('"', '').split(','))
    categories = [category.strip() for category in categories]
    return categories


def postprocess_properties(properties_dict):
    if 'categories' in properties_dict and properties_dict['categories']:
        properties_dict['categories'] = split_categories(properties_dict['categories'])
    else:
        properties_dict['categories'] = None

    # add download
    if 'download' not in properties_dict:
        properties_dict['download'] = properties_dict['source'][:properties_dict['source'].rfind('.')] + '.zip'


if __name__ == "__main__":
    if len(argv) < 2:
        print("script takes json string as argument.\nStopping...")
        raise ValueError

    props = json.loads(argv[1])
    postprocess_properties(props)

    # open database
    database_file = pathlib.Path(__file__).parent.parent / 'contributions.yaml'

    yaml = YAML()
    with open(database_file, 'r') as db:
        data = yaml.load(db)

    contributions_list = list(data['contributions'])

    # find max index
    max_index = max([int(contribution["id"]) for contribution in contributions_list])

    # append new contribution with next index
    # add status, at top
    datetime_today = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
    contribution = {
        'id': max_index + 1,
        'status': 'VALID',
        'dateAdded': datetime_today,
    }
    contribution.update(props)

    contributions_list.append(contribution)

    # write all contributions to database file
    with open(database_file, 'w') as db:
        yaml.dump({"contributions": contributions_list}, db)
