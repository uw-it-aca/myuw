# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


class DisabledAction(Exception):
    """
    Disallowed action when overriding
    """
    pass


class InvalidInputFormData(Exception):
    """
    malformed syntax in the form input data
    """
    pass


class NotInstructorError(Exception):
    """
    Unauthorized (not instructor of the course)
    """
    pass
