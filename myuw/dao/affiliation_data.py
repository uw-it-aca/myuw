import os
import csv
from myuw.exceptions import InvalidAffiliationDataFile


def get_data_for_affiliations(model=None, file=None, affiliations=None,
                              unique=None):
    data = []
    matched_data = []

    if affiliations is None:
        affiliations = {}

    if file:
        data = _load_data_from_file(file)
    elif model:
        data = _load_data_from_model(model)

    unique_lookup = set()
    for entry in data:
        if entry['campus']:
            if entry['campus'] not in affiliations:
                continue
        if entry['pce'] is True:
            if 'pce' not in affiliations or not affiliations['pce']:
                continue
        if entry['pce'] is False:
            if 'pce' in affiliations and affiliations['pce']:
                continue

        if entry['affiliation']:
            if entry['affiliation'] not in affiliations:
                continue

        if unique:
            value = unique(entry['all_data'])
            if value in unique_lookup:
                continue
            unique_lookup.add(value)
        matched_data.append(entry['all_data'])

    return matched_data


def _load_data_from_model(model):
    all_instances = model.objects.all()
    all_data = []
    for obj in all_instances:
        all_data.append({
            'campus': obj.campus,
            'affiliation': obj.affiliation,
            'pce': obj.pce,
            'all_data': obj,
        })
    return all_data


def _load_data_from_file(file_name):
    """
    Loads affiliation-based data from a file.  Path is relative to myuw/data
    """
    all_data = []

    path = os.path.join(os.path.dirname(__file__), '..', 'data', file_name)
    with open(path, 'rbU') as csvfile:
        reader = csv.DictReader(csvfile)
        for name in ('campus', 'affiliation', 'pce'):
            if name not in reader.fieldnames:
                raise InvalidAffiliationDataFile("Missing header: %s" % name)

        for row in reader:
            campus = row['campus']
            affiliation = row['affiliation']
            pce = row['pce']

            if "" == campus or "all" == campus:
                campus = None

            if "" == affiliation or "all" == affiliation:
                affiliation = None

            if "yes" == pce:
                is_pce = True
            elif "no" == pce:
                is_pce = False
            elif "" == pce or "all" == pce:
                is_pce = None
            else:
                raise InvalidAffiliationDataFile("Bad pce data: %s" % pce)

            all_data.append({
                'campus': campus,
                'affiliation': affiliation,
                'pce': is_pce,
                'all_data': row,
            })

    return all_data
