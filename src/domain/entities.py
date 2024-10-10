import dataclasses

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

    @contract(DomainInvariant)
    def __post_init__(self):
        assert self.price >= 0, "Price can not be negative"
        assert 0 <= self.discount <= 100, "Discount need to be in range [0, 100]"
        assert self.available >= 0, "Available can not be negative"
        assert self.reserved >= 0, "Reserved can not be negative"

    @contract(DomainInvariant)
    def reserve(self, quantity: int):
        assert self.available >= quantity, "Not enough products in stock"

        self.available -= quantity
        self.reserved += quantity

    @contract(DomainInvariant)
    def unreserve(self, quantity: int):
        assert self.reserved >= quantity, "Not enough products reserved"

        self.available += quantity
        self.reserved -= quantity

    @contract(DomainInvariant)
    def sell(self, quantity: int):
        assert self.available >= quantity, "Not enough products in stock"

        self.available -= quantity

    @contract(DomainInvariant)
    def set_price(self, price: float):
        assert price >= 0, "Price can not be negative"
        self.price = price

    @contract(DomainInvariant)
    def set_discount(self, discount: int):
        assert 0 <= discount <= 100, "Discount need to be in range [0, 100]"
        self.discount = discount

    @property
    def final_price(self):
        return self.price - (self.price * self.discount) / 100


@dataclasses.dataclass
class SelectedProductItems:
    customer_id: int
    product_id: int
    quantity: int

    @contract(DomainInvariant)
    def __post_init__(self):
        assert self.quantity > 0, "Quantity can not be zero or negative"


@dataclasses.dataclass
class CompletedOrder(SelectedProductItems):
    pass
