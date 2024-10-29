"""
Reads a properties txt file from a library's release artifacts,
and validates the contents. If valid, it returns the contents
as an object.

TODO: write tests for validation
"""
import json
import argparse

import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import re
import os
from typing import Optional, Union
from pydantic import BaseModel, Field, ConfigDict, field_validator


class PropertiesBase(BaseModel):
    name: str
    authors: str
    url: str
    categories: Optional[str] = Field(None)
    sentence: str
    paragraph: Optional[str] = None
    version: int
    prettyVersion: str
    minRevision: int = Field(0)
    maxRevision: int = Field(0)

    model_config = ConfigDict(
        extra='allow',
    )

class PropertiesExisting(PropertiesBase):
    authors: str = Field(alias='authorList')
    categories: Optional[str] = Field(None, alias='category')
    version: Union[int, str]
    prettyVersion: Optional[str] = None

    model_config = ConfigDict(
        extra='allow',
        populate_by_name=True,
    )

    @field_validator('minRevision', 'maxRevision', mode='before')
    def default_on_error(cls, v):
        if v.isdigit():
            return int(v)
        else:
            return 0


class LibraryPropertiesNew(PropertiesBase):
    categories: str


@retry(stop=stop_after_attempt(3),
       wait=wait_fixed(2),
       reraise=True)
def read_properties_txt(properties_url):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'text/html',
    }
    r = requests.get(properties_url, headers=headers)

    if r.status_code != 200:
        raise FileNotFoundError(f"status code {r.status_code} returned for url {r.url}")

    return r.text

def parse_text(properties_raw):
    field_pattern = re.compile(r"^([a-zA-z]+)\s*=(.*)")

    properties_dict = {}
    field_name = ""
    field_value = ""
    properties_lines = properties_raw.split('\n')
    for line in properties_lines:
        if line.startswith('#') or not line.strip():
            continue
        if line_match := field_pattern.match(line):
            # store previous key-value pair
            if field_name:
                properties_dict[field_name] = field_value
            # process current line
            field_name = line_match[1].strip()
            field_value = line_match[2].strip()
            field_value = field_value.split('#')[0].strip()
        else:
            field_value += " " + line.strip()
    # store last key-pair
    if field_name:
        properties_dict[field_name] = field_value

    print(f"properites_dict={properties_dict}")
    return properties_dict

def validate_existing(properties_dict):
    # validation on existing contribution is weaker
    properties = PropertiesExisting.model_validate(properties_dict)

    return properties.model_dump()

def validate_new(properties_dict):
    # new contribution has stronger validation
    properties = PropertiesBase.model_validate(properties_dict)

    return properties.model_dump()

def validate_new_library(properties_dict):
    # new contribution has stronger validation
    properties = LibraryPropertiesNew.model_validate(properties_dict)

    return properties.model_dump()

def set_output(output_object):
    with open(os.environ['GITHUB_OUTPUT'],'a') as f:
        f.write(f'props={json.dumps(output_object)}')

def set_output_error(msg):
    with open(os.environ['GITHUB_OUTPUT'],'a') as f:
        f.write(f'error={msg}')


if __name__ == "__main__":
    # this is used by github workflow, on new contributions. Use strong validation.
    # Add type to object
    parser = argparse.ArgumentParser()
    parser.add_argument('type')
    parser.add_argument('url')
    args = parser.parse_args()

    type_ = args.type
    url = args.url
    if not url.startswith("http"):
        print(f"Url not valid: {url}.\nStopping...")
        set_output_error(f"Url is not valid. It should start with http:// or https://")
        raise AssertionError

    print(f"url: {url}")  # just for debugging, should do this via logging levels

    try:
        properties_raw = read_properties_txt(url)
    except Exception as e:
        set_output_error(f'Error when accessing url. Please ensure the url returns a valid properties text file')
        raise e

    print(f"properties text: {properties_raw}")  # just for debugging, should do this via logging levels

    try:
        if type_ == 'library':
            props = validate_new_library(parse_text(properties_raw))
        else:
            props = validate_new(parse_text(properties_raw))
    except Exception as e:
        set_output_error(f'Errors when parsing file. Please check all required fields, and file format.\n\n{e}')
        raise e

    contribution= {
        "type": type_,
        "source": url,
    }
    contribution.update(props)

    print(f"properties dict: {contribution}")  # just for debugging, should do this via logging levels
    set_output(contribution)
