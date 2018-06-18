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
