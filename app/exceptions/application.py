class ApplicationAlreadyExistsException(Exception):
    pass


class ApplicationNotFoundException(Exception):
    pass


class InvalidApplicationStatusTransitionException(Exception):
    pass


class InvalidApplicationStatusException(Exception):
    pass


class ApplicationNotEditableException(Exception):
    pass
