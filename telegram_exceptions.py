class CurrencyException(Exception):
    pass


class TooManyValuesException(CurrencyException):
    pass


class SameCurrencyError(CurrencyException):
    pass
