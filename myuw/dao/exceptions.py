"""
Contains the custom exceptions used by the restclients.
"""


class EmailServiceUrlException(Exception):
    """Unhandled email domain or malformed email address"""
    pass


class CanavsNonSWSException(Exception):
    """Non-academic (adhoc) Canvas course"""
    pass
