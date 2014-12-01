from django.utils.importlib import import_module
from django.conf import settings
from django.core.exceptions import *
from restclients.dao import MY_DAO
from myuw_mobile.restclients.dao_implementation.hfs import File as HfsFile


class Hfs_DAO(MY_DAO):
    def getURL(self, url, headers):
        return self._getURL('hfs', url, headers)

    def _getDAO(self):
        return self._getModule('RESTCLIENTS_HFS_DAO_CLASS', HfsFile)
