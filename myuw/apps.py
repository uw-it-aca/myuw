from __future__ import unicode_literals
from django.apps import AppConfig
from restclients_core.dao import MockDAO
import os


class MyUWConfig(AppConfig):
    name = 'myuw'

    def ready(self):
        myuw_mocks = os.path.join(os.path.dirname(__file__), "resources")
        MockDAO.register_mock_path(myuw_mocks)
