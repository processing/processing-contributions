"""
Creates the json files in the sources folder from the contributions.yaml file.
"""

import json
import pathlib
import shutil

from utils import get_valid_contributions

json_fields_library = [
    'name', 'authors', 'url', 'categories', 'sentence', 'paragraph', 'imports',
    'id', 'type'
]
json_fields_example = [
    'name', 'authors', 'url', 'categories', 'sentence', 'modes', 'paragraph', 'imports',
    'id', 'type'
]
json_fields_tool = [
    'name', 'authors', 'url', 'categories', 'sentence', 'paragraph', 'imports',
    'id', 'type'
]
json_fields_mode = [
    'name', 'authors', 'url', 'sentence', 'paragraph', 'imports',
    'id', 'type', 'categories'
]
json_package_fields_list = ['mode', 'minRevision', 'maxRevision', 'props', 'download']


def to_sources_dict(contribution_dict):
  contribution_dict['props'] = contribution_dict.pop('source')
  if contribution_dict['type'] == 'library':
    sources_dict = {
      field: contribution_dict[field]
      for field in json_fields_library if field in contribution_dict
    }
  elif contribution_dict['type'] == 'examples':
    sources_dict = {
        field: contribution_dict[field]
        for field in json_fields_example if field in contribution_dict
    }
  elif contribution_dict['type'] == 'tool':
    sources_dict = {
      field: contribution_dict[field]
      for field in json_fields_tool if field in contribution_dict
    }
  else:
    sources_dict = {
      field: contribution_dict[field]
      for field in json_fields_mode if field in contribution_dict
    }

  # put authors in list
  sources_dict['authors'] = [sources_dict['authors']] if sources_dict['authors'] else sources_dict['authors']

  sources_dict['packages'] = [
    {
      field:('java' if field == 'mode' else str(contribution_dict[field]))
      for field in json_package_fields_list
    }
  ]

  return sources_dict


if __name__ == "__main__":
  sources_folder = pathlib.Path(__file__).parent.parent / 'sources/'

  contributions_list = get_valid_contributions()

  # remove sources folder if it already exists
  if sources_folder.is_dir():
    shutil.rmtree(sources_folder)
  sources_folder.mkdir(parents=True, exist_ok=True)

  # create a json file in the sources folder for each contribution
  for contribution in contributions_list:
    if 'name' in contribution:
      # output zero padded string for id
      contribution['id'] = f"{contribution['id']:03}"
      filename = contribution['name'].replace(':','').replace('/','').replace(' ','_') + '.json'
      this_filepath = sources_folder / filename
      with open(this_filepath, 'w') as f:
        json.dump(to_sources_dict(contribution),f,indent=2)
