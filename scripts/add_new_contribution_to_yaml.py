"""
given properties, add a new contribution to the contributions.yaml database file.
"""
import json
from sys import argv

from ruamel.yaml import YAML

if __name__ == "__main__":
    if len(argv) < 2:
        print("script takes json string as argument.\nStopping...")
        raise ValueError

    props = json.loads(argv[1])
    # process category list
    if props['categories']:
        props['categories'] = sorted(props['categories'].replace('"', '').split(','))
        props['categories'] = [category.strip() for category in props['categories']]
    else:
        props['categories'] = None

    # add download
    if 'download' not in props:
        props['download'] = props['source'][:props['source'].rfind('.')] + '.zip'

    # open database
    database_file = '../contributions.yaml'

    yaml = YAML()
    with open(database_file, 'r') as db:
        data = yaml.load(db)

    contributions_list = list(data['contributions'])

    # find max index
    max_index = max([int(contribution["id"]) for contribution in contributions_list])

    # append new contribution with next index
    # add status, at top
    contribution = {
        'id': max_index + 1,
        'status': 'VALID',
    }
    contribution.update(props)

    contributions_list.append(contribution)

    # write all contributions to database file
    with open(database_file, 'w') as db:
        yaml.dump({"contributions": contributions_list}, db)
