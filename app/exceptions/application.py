class ApplicationAlreadyExistsException(Exception):
    pass


class ApplicationNotFoundException(Exception):
    pass


class InvalidApplicationStatusTransitionException(Exception) :
    pass 