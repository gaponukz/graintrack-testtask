import dataclasses
import typing

from src.domain import DomainInvariant, contract


@dataclasses.dataclass
class CreateProductInputDTO:
    name: str
    price: float
    subcategory_id: int
    available: int

    @contract(DomainInvariant)
    def __post_init__(self):
        assert self.price >= 0, "Price can not be negative"
        assert self.available >= 0, "Available can not be negative"


@dataclasses.dataclass
class CreateProductOutputDTO:
    product_id: int


@dataclasses.dataclass
class GetProductsInputDTO:
    category_id: typing.Optional[int] = None
    subcategory_id: typing.Optional[int] = None


@dataclasses.dataclass
class EditProductInputDTO:
    product_id: int
    price: typing.Optional[float] = None
    discount: typing.Optional[int] = None


@dataclasses.dataclass
class CancelReservationInputDTO:
    customer_id: int
    product_id: int


@dataclasses.dataclass
class GetSellReportInputDTO:
    limit: int
    offset: int
    category_id: typing.Optional[int] = None
    subcategory_id: typing.Optional[int] = None


@dataclasses.dataclass
class GetSellReportItem:
    category_name: str
    subcategory_name: str
    quantity: int
    total: float


class GetSellReportOutputDTO(list[GetSellReportItem]):
    pass
