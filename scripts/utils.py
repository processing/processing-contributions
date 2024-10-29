from ruamel.yaml import YAML

database_file = '../contributions.yaml'


def get_contributions():
    # read in database yaml file
    yaml = YAML()
    with open(database_file, 'r') as db:
        data = yaml.load(db)

    contributions_list = data['contributions']

    # filter contributions list, remove contribution status == BROKEN
    contributions_list = [
        contribution for contribution in contributions_list if contribution['status'] not in ["BROKEN", "DEPRECATED"]
    ]

    return contributions_list


def apply_override(contributions_list):
    # apply override. if field additional_category, add value to categories
    for contribution in contributions_list:
        if 'override' in contribution.keys():
            for key in contribution['override'].keys():
                contribution[key] = contribution['override'][key]


def get_valid_contributions():
    contributions = get_contributions()
    apply_override(contributions)

    return contributions