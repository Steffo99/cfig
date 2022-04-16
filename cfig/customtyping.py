import typing as t

TYPE = t.TypeVar("TYPE")


class Resolver(t.Protocol):
    __name__: str
    __doc__: str

    def __call__(self, val: t.Any) -> TYPE:
        ...


class ResolverRequired(Resolver):
    def __call__(self, val: str) -> TYPE:
        ...


class ResolverOptional(Resolver):
    def __call__(self, val: t.Optional[str]) -> TYPE:
        ...


__all__ = (
    "TYPE",
    "Resolver",
    "ResolverRequired",
    "ResolverOptional",
)
