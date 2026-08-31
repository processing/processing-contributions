"""
Creates the contribs.txt file from the contributions.yaml file.
"""

import json
import pathlib
import shutil
from collections import defaultdict
from typing import List

from utils import get_valid_contributions

type_list = ['library', 'examples', 'tool', 'mode']
contribs_fields_list = [
    'name', 'authors', 'url', 'categories', 'sentence', 'paragraph',
    'version', 'prettyVersion', 'minRevision', 'maxRevision', 'imports',
    'modes', 'compatibleModesList', 'id', 'type', 'download'
]


def read_contribs_text(filepath):
  contribs_list = []
  this_contrib = {}
  contrib_empty = True
  contrib_field_counts = defaultdict(int)

  with open(filepath, 'r') as f:
    for line in f.readlines():
      if line.strip() == "":
        if not contrib_empty:
          for key in list(this_contrib.keys()):
            contrib_field_counts[key] += 1
          contribs_list.append(this_contrib)
          this_contrib = {}
          contrib_empty = True

      str_index = line.find("=")  # capture first equals,
      if str_index >= 0:
        field, value = line.split("=", 1)
        this_contrib[field.strip()] = value.strip()
        contrib_empty = False

  with open("contribs_txt_field_counts.json", 'w') as f:
    json.dump(contrib_field_counts, f)

  return contribs_list


def preprocess_contributions() -> List:
  all_contributions = get_valid_contributions()

  # sort contributions list by type
  def sort_key(d):
    return type_list.index(d['type'])
  all_contributions = sorted(all_contributions, key=sort_key)

  return all_contributions


def write_contribs(all_contributions, fh):
  for contribution in all_contributions:
    fh.write(contribution['type'] + '\n')
    for field in contribs_fields_list:
      if field in contribution:
        if field == 'id':
          fh.write(f'{field}={contribution[field]:03}\n')
        elif field == 'categories':
          if contribution['type'] == 'library':
            fh.write(f'{field}={",".join(contribution[field]) if contribution[field] else ""}\n')
          else:
            # categories are only relevant for libraries, except for examples with "Books" as category
            if contribution[field] and 'Books' in contribution[field]:
              fh.write(f'{field}={",".join(contribution[field]) if contribution[field] else ""}\n')
            else:
              fh.write(f'{field}=\n')
        elif field == 'compatibleModesList':
          fh.write(f'modes={contribution[field]}\n')
        else:
          fh.write(f'{field}={"" if contribution[field] is None else contribution[field]}\n')
    fh.write('\n')


if __name__ == "__main__":
  pde_folder = pathlib.Path(__file__).parent.parent / 'pde/'
  # remove sources folder if it already exists
  if pde_folder.is_dir():
    shutil.rmtree(pde_folder)
  pde_folder.mkdir(parents=True, exist_ok=True)

  contribs_text_file = pde_folder / 'contribs.txt'

  contributions_list = preprocess_contributions()

  # write contribs.txt file
  with open(contribs_text_file, 'w+') as f:
    write_contribs(contributions_list, f)


