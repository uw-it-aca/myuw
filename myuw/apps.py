# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os

from django.apps import AppConfig
from restclients_core.dao import MockDAO


class MyUWConfig(AppConfig):
    name = 'myuw'

    def ready(self):
        myuw_mocks = os.path.join(os.path.dirname(__file__), "resources")
        MockDAO.register_mock_path(myuw_mocks)
