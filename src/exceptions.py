"""Shared exceptions for the currency exchange bot."""


class ExchangeRateError(Exception):
    """Raised when an exchange-rate source cannot be fetched or parsed."""
