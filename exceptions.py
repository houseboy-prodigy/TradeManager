# define Python user-defined exceptions
class QuantityError(Exception):
    """Base class for other exceptions"""
    pass


class BalanceError(Exception):
    """Raised when the input value is too small"""
    pass


class TooManyRequestsError(Exception):
    """Raised when the input value is too large"""
    pass

class DecimalError(Exception):
    """Raised when the input value is too large"""
    pass
