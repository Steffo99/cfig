"""
This module extends :mod:`typing` with the types used by :mod:`cfig`.
"""


import typing as t


TYPE = t.TypeVar("TYPE")


ResolverAny = t.Callable[[t.Any], TYPE]
ResolverRequired = t.Callable[[str], TYPE]
ResolverOptional = t.Callable[[t.Optional[str]], TYPE]
ProxyAny = t.Callable[[t.Callable[[t.Any], TYPE]], TYPE]
ProxyRequired = t.Callable[[t.Callable[[str], TYPE]], TYPE]
ProxyOptional = t.Callable[[t.Callable[[t.Optional[str]], TYPE]], TYPE]


__all__ = (
    "TYPE",
    "ResolverAny",
    "ResolverRequired",
    "ResolverOptional",
    "ProxyAny",
    "ProxyRequired",
    "ProxyOptional",
)
