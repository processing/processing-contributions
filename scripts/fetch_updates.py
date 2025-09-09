"""
Reads in the contributions.yaml file, and updates the entries by hitting the 'source' url.
"""
import argparse
from datetime import datetime, UTC
import pathlib
from ruamel.yaml import YAML
from multiprocessing import Pool

from parse_and_validate_properties_txt import read_properties_txt, parse_text, validate_existing


def update_contribution(contribution, props):
  datetime_today = datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
  contribution['lastUpdated'] = datetime_today
  if 'previousVersions' not in contribution:
    contribution['previousVersions'] = []
  contribution['previousVersions'].append(contribution['prettyVersion'])

  # update from online
  for field in props.keys():
    # process category list
    if field == 'categories':
      if props[field]:
        contribution[field] = sorted(props[field].strip('"').split(','))
      else:
        contribution[field] = []
    else:
      contribution[field] = props[field]

  if 'download' not in contribution:
    contribution['download'] = contribution['source'][:contribution['source'].rfind('.')] + '.zip'
    

def log_broken(contribution, msg):
  if contribution['status'] == 'VALID':
    contribution['status'] = 'BROKEN'
    if 'log' not in contribution:
      contribution['log'] = []
    contribution['log'].append(msg)

def process_contribution(item):
  index, contribution = item

  date_today = datetime.now(UTC).strftime('%Y-%m-%d')
  this_version = '0'

  if contribution['status'] != 'DEPRECATED':
    # compare version to what is at url. If has changed, update contribution to
    # what is online
    if 'version' in contribution:
      this_version = contribution['version']

    try:
      properties_raw = read_properties_txt(contribution['source'])
    except FileNotFoundError as e:
      log_broken(contribution, f'file not found, {e}, {date_today}')
      return index, contribution
    except Exception:
      log_broken(contribution, f'url timeout, {date_today}')
      return index, contribution

    try:
        props = validate_existing(parse_text(properties_raw))
    except Exception:
      log_broken(contribution, f'invalid file, {date_today}')
      return index, contribution

    # some library files have field lastUpdated. This also exists in the database, but is defined
    # by our scripts, so remove this field.
    contribution.pop('lastUpdated', None)

    contribution['status'] = 'VALID'

    if props['version'] != this_version:
      # update from online
      update_contribution(contribution, props)
  return index, contribution


def process_all(contributions_list):
  total = len(contributions_list)
  completed = 0
  print(f"Starting processing of {total} contributions...")

  with Pool(processes=256) as pool:
    for index, contribution in pool.imap_unordered(process_contribution, enumerate(contributions_list)):
      contributions_list[index] = contribution
      completed += 1
      print(f"Progress: {completed}/{total} ({(completed / total * 100):.1f}%)")


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--index')
  args = parser.parse_args()

  index = 'all'
  if args.index:
    index = args.index

  database_file = pathlib.Path(__file__).parent.parent / 'contributions.yaml'

  # read in database yaml file
  yaml = YAML()
  with open(database_file, 'r') as db:
    data = yaml.load(db)

  contributions_list = data['contributions']

  if index == 'all':
    process_all(contributions_list)
    print("All processing complete")
  else:
    # update only contribution with id==index
    contribution = next((x for x in contributions_list if x['id'] == int(index)), None)
    print(contribution)
    process_contribution((index, contribution))
    print(contribution)

  # write all contributions to database file
  yaml = YAML()
  with open(database_file, 'w') as outfile:
    yaml.dump({"contributions": contributions_list}, outfile)
