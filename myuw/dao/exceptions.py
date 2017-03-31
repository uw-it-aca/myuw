"""
Contains the custom exceptions used by the restclients.
"""


class EmailServiceUrlException(Exception):
    """Unhandled email domain or malformed email address"""
    pass


class CanvasNonSWSException(Exception):
    """Non-academic (adhoc) Canvas course"""
    pass


class NotSectionInstructorException(Exception):
    """Request for section data from non-instructor"""
    pass


class IndeterminateCampusException(Exception):
    """Cannot determine campus from registrations or PWS"""
    pass
