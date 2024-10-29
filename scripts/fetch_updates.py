"""
Reads in the contributions.yaml file, and updates the entries by hitting the 'source' url.
"""
import argparse
from datetime import datetime
from ruamel.yaml import YAML

from parse_and_validate_properties_txt import read_properties_txt, parse_text, validate_existing


def update_contribution(contribution, props):
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
    contribution['log'].append(msg)

def process_contribution(contribution):
  date_today = datetime.today().strftime('%Y-%m-%d')
  this_version = 0

  if contribution['status'] != 'DEPRECATED':
    # compare version to what is at url. If has iterated up, update contribution to
    # what is online
    if 'version' in contribution:
      this_version = int(contribution['version'])

    try:
      properties_raw = read_properties_txt(contribution['source'])
    except FileNotFoundError as e:
      log_broken(contribution, f'file not found, {e}, {date_today}')
      return
    except Exception:
      log_broken(contribution, f'url timeout, {date_today}')
      return

    try:
        props = validate_existing(parse_text(properties_raw))
    except Exception:
      log_broken(contribution, f'invalid file, {date_today}')
      return

    if int(props['version']) > this_version:
      # update from online
      update_contribution(contribution, props)
      contribution['status'] = 'VALID'


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--index')
  args = parser.parse_args()

  index = 'all'
  if args.index:
    index = args.index

  database_file = '../contributions.yaml'

  # read in database yaml file
  yaml = YAML()
  with open(database_file, 'r') as db:
    data = yaml.load(db)

  contributions_list = data['contributions']

  if index == 'all':
    # update all contributions
    for contribution in contributions_list:
      process_contribution(contribution)
  else:
    # update only contribution with id==index
    contribution = next((x for x in contributions_list if x['id'] == int(index)), None)
    print(contribution)
    process_contribution(contribution)
    print(contribution)

  # write all contributions to database file
  yaml = YAML()
  with open(database_file, 'w') as outfile:
    yaml.dump({"contributions": contributions_list}, outfile)
