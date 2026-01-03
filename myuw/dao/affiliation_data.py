# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
import csv
from myuw.dao.exceptions import InvalidAffiliationDataFile


def get_data_for_affiliations(model=None, file=None, affiliations={},
                              unique=None, **filters):
    data = []
    matched_data = []

    if file:
        data = _load_data_from_file(file)
    elif model:
        data = _load_data_from_model(model, **filters)

    unique_lookup = set()
    for entry in data:
        # MUWM-5417
        required_aff = entry.get('affiliation')
        required_campus = entry.get('campus')

        if required_aff and required_campus:
            if (
                not affiliations or
                not affiliations.get(required_aff) or
                not affiliations.get(required_campus)
            ):
                continue

            if (affiliations.get(required_aff) and
                    affiliations.get(required_campus)):
                pass
        elif required_campus:
            if not affiliations or not affiliations.get(required_campus):
                continue
        elif required_aff:
            if not affiliations or not affiliations.get(required_aff):
                continue

        if entry.get('pce'):
            if not affiliations or not affiliations.get('pce'):
                continue

        if unique:
            value = unique(entry['all_data'])
            if value in unique_lookup:
                continue
            unique_lookup.add(value)
        matched_data.append(entry['all_data'])

    return matched_data


def _load_data_from_model(model, **filters):
    all_instances = model.objects.filter(**filters)
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
    with open(path, 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for name in ('campus', 'affiliation', 'pce'):
            if name not in reader.fieldnames:
                raise InvalidAffiliationDataFile(
                    "Missing header: {}".format(name))

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
                raise InvalidAffiliationDataFile(
                    "Bad pce data: {}".format(pce))

            all_data.append({
                'campus': campus,
                'affiliation': affiliation,
                'pce': is_pce,
                'all_data': row,
            })

    return all_data
