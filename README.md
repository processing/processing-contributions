# [WIP] processing-contributions

[!WARNING]
This repository is a work in progress.

This repository maintains the contributions to Processing.

All contributions are stored in a contributions database file in yaml format, `contributions.yaml`.
Consumers of this data are the Processing website, and the Processing application.

Within the `scripts` folder are scripts for parsing and validating the data from the 
properties file. These are used by a Github action to processing new contributions and add them to the
database. The `issue_to_pr.yml` workflow is triggered by a new issue for registering a new contribution.
It will then retrieve the properties file provided in the issue, parse and validate, and then if valid,
add the new information to the `contributions.yaml` database file in a new pull request.

## Data structure
All contributions are stored in a contributions database file in yaml format, `contributions.yaml`.
Each entry contains the fields found in the properties file, such as
* The fields from the `library.properties` file are: `name`, `version`, `prettyVersion`, 
`minRevision`, `maxRevision`, `authors`, `url`, `type`, `categories`, `sentence`, `paragraph`. These
fields will also be in the database, and will be the value in the library property text file. If
any of these values should be overridden, please read below about the `override` field.

Additional fields are
* `id`: integer value id. 
* `source`: url of the properties file, from the published library
* `download`: url of the zip file containing the library
* `status` - Possible values are 
   * `DEPRECATED` - Libraries that seem to be permanently down, or have been deprecated. 
   These are libraries that are commented out of `source.conf`. This is manually set.
   * `BROKEN` - libraries whose properties file cannot be retrieved, but we will still check. 
   These are libraries listed in `skipped.conf`
   * `VALID` - libraries that are valid and available
* `override` - This is an object, where any component field values will replace the existing field values. For example, libraries in the `broken.conf` file are outdated, and we want to cap the
`maxRevision` to `228`. This cap can be applied by setting `override` to {`maxRevision`: `228`}
* `log` - Any notes of explanation, such as why a library was labeled `BROKEN`

## Scripts
The scripts folder contains scripts in Python for parsing, validating, and processing the database 
file and properties files.

* `add_new_contribution_to_yaml.py`: script to be used from command line, that is called only by the 
issue_to_pr Github workflow. It takes two arguments:
  * contribution type - such as `library`, `examples`, `tool` or `mode`.
  * source url - the url for the properties file in the published library to be added as a new contribution.
* `fetch_updates.py`: script that can be called from command line, that will update a specified contribution (via id)
or it will update the full contributions database file. It will update by retrieving the content in the `source` url.
If the version has iterated, it will overwrite the previous entry in the database file.
* `parse_and_validate_properties_txt.py`: tools for parsing and validating properties text files. the `issue_to_pr`
Github workflow will call this from command line. If the data is valid, this will set an environment variable in 
the workflow environment to the contribution object.
* `to_contribs_txt.py`: processes the `contributions.yaml` database file to `pde/contribs.txt` for consumption
by the contribution manager in the Processing application.
* `to_sources_jsons.py`: processes the `contributions.yaml` database file to individual json files in the `sources` 
folder, for consumption by the Processing website.
* `utils.py`: utility functions used by multiple script files.


## Outputs

At this time, the website requires a folder of json files, where each json file is a separate 
contribution. These files are created from the database using the script `scripts/to_source_jsons.py`.

The Processing application's contribution manager reads in a `contribs.txt` file.
This file is created from the database using the script `scripts/to_contribs_txt.py`.


## Contributors

This repository was created by Claudine Chen ([@mingness](https://github.com/mingness)) as part of the 
2024 New Beginnings (pr05) Grant from the [Processing Foundation](https://github.com/processing), to simplify the
workflows for libraries, tools, and modes, mentored by Stef Tervelde ([@Stefterv](https://github.com/stefterv)).
