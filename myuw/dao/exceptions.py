"""
Contains the custom exceptions used by the restclients.
"""


class EmailServiceUrlException(Exception):
    """Unhandled email domain or malformed email address"""
    pass


class UnsupportedAffiliationException(Exception):
    """User not associated with supported affiliation"""
    pass
