# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

"""
Contains the custom exceptions used by the restclients.
"""


class EmailServiceUrlException(Exception):
    """Unhandled email domain or malformed email address"""


class CanvasNonSWSException(Exception):
    """Non-academic (adhoc) Canvas course"""


class NotSectionInstructorException(Exception):
    """Request for section data from non-instructor"""


class CourseRequestEmailRecipientNotFound(Exception):
    """MAILMAN_COURSEREQUEST_RECIPIENT not in Settings"""


class IndeterminateCampusException(Exception):
    """Cannot determine campus from registrations or PWS"""


class InvalidAffiliationDataFile(Exception):
    pass


class InvalidResourceCategory(Exception):
    pass


class BlockedNetidErr(Exception):
    pass
