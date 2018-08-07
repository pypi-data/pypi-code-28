"""
 A collection of helper classes for dealing with everything granule related.
 Hopefully this can be expanded on in the future to add support for different
 types of granules such as the legacy granules
"""

from .granules import SentinelGranule
from .pairs import GranulePair, SentinelGranulePair
from .stack import GranuleStack, SentinelGranuleStack
from .exceptions import InvalidGranuleException, InvalidCredentialsException
from .download import download


__all__ = [
    "SentinelGranule", "GranulePair",
    "SentinelGranulePair", "GranuleStack", "SentinelGranuleStack",
    "download",
    "InvalidGranuleException", "InvalidCredentialsException"
]
