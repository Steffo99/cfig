import typing as t

TYPE = t.TypeVar("TYPE")


class Configurable(t.Protocol):
    __name__: str
    __doc__: str

    def __call__(self, val: t.Any) -> TYPE:
        ...


class ConfigurableRequired(Configurable):
    def __call__(self, val: str) -> TYPE:
        ...


class ConfigurableOptional(Configurable):
    def __call__(self, val: t.Optional[str]) -> TYPE:
        ...


__all__ = (
    "TYPE",
    "Configurable",
    "ConfigurableRequired",
    "ConfigurableOptional",
)
