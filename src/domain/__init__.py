import dataclasses
import functools
import typing

from src.domain.errors import ValidationError


@dataclasses.dataclass
class ContractBody:
    exception: type[Exception]


DomainInvariant = ContractBody(exception=ValidationError)


F = typing.TypeVar("F", bound=typing.Callable)


def contract(body: ContractBody):
    def _contract(function: F) -> F:
        @functools.wraps(function)
        def decorator(*args, **kwargs):
            try:
                return function(*args, **kwargs)

            except AssertionError as error:
                raise body.exception(str(error))

        return typing.cast(F, decorator)

    return _contract
