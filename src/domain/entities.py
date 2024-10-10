import dataclasses
import typing

from src.domain import DomainInvariant, contract


@dataclasses.dataclass
class Category:
    id: int
    name: str


@dataclasses.dataclass
class SubCategory:
    id: int
    name: str
    category_id: int


@dataclasses.dataclass
class Product:
    id: int
    name: str
    price: float
    subcategory_id: int
    available: int
    reserved: int
    discount: int = 0

    def __post_init__(self):
        self.validate_price()
        self.validate_quantity()

    @contract(DomainInvariant)
    def validate_quantity(self):
        assert self.available >= 0, "Available can not be negative"
        assert self.reserved >= 0, "Reserved can not be negative"

    @contract(DomainInvariant)
    def validate_price(self):
        assert self.price >= 0, "Price can not be negative"
        assert 0 <= self.discount <= 100, "Discount need to be in range [0, 100]"

    @property
    def final_price(self):
        return self.price - (self.price * self.discount) / 100


class _QuantityProtocol(typing.Protocol):
    quantity: int


class _QuantityAble(_QuantityProtocol):
    @contract(DomainInvariant)
    def __post_init__(self):
        assert self.quantity > 0, "Quantity can not be zero or negative"


@dataclasses.dataclass
class Reservation(_QuantityAble):
    customer_id: int
    product_id: int
    quantity: int


@dataclasses.dataclass
class CompletedOrder(_QuantityAble):
    customer_id: int
    product_id: int
    quantity: int
