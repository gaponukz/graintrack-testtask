import dataclasses

import pytest

from src.application.dto import CreateProductInputDTO, GetProductsInputDTO
from src.application.persistent import (
    CompletedOrderRepository,
    ProductRepository,
    ReservationRepository,
    UnitOfWork,
)
from src.domain.entities import CompletedOrder, Product, SelectedProductItems


class MemoryProductRepository(ProductRepository):
    def __init__(self):
        self.products: dict[int, Product] = {}
        self.last_id = 1

    def create(self, product: CreateProductInputDTO) -> int:
        product_id = self.last_id
        self.products[product_id] = Product(
            id=product_id,
            name=product.name,
            price=product.price,
            subcategory_id=product.subcategory_id,
            available=product.available,
            reserved=0,
        )
        self.last_id += 1

        return product_id

    def get_list(self, _: GetProductsInputDTO) -> list[Product]:
        return list(self.products.values())

    def get(self, product_id: int, for_update: bool = False) -> Product:
        return dataclasses.replace(self.products[product_id])

    def update(self, product: Product):
        self.products[product.id] = dataclasses.replace(product)

    def delete(self, product_id: int):
        del self.products[product_id]


class MemoryReservationRepository(ReservationRepository):
    def __init__(self):
        self.reservations: dict[tuple[int, int], int] = {}

    def create(self, reservation: SelectedProductItems):
        self.reservations[(reservation.customer_id, reservation.product_id)] = (
            reservation.quantity
        )

    def get(self, customer_id: int, product_id: int) -> SelectedProductItems:
        quantity = self.reservations[(customer_id, product_id)]

        return SelectedProductItems(
            customer_id=customer_id,
            product_id=product_id,
            quantity=quantity,
        )

    def delete(self, customer_id: int, product_id: int):
        del self.reservations[(customer_id, product_id)]


class MemoryCompletedOrderRepository(CompletedOrderRepository):
    def __init__(self):
        self.orders: list[CompletedOrder] = []

    def create(self, order: CompletedOrder):
        self.orders.append(order)


class MemoryUnitOfWork:
    def __init__(self):
        self.product_repository = MemoryProductRepository()
        self.reservation_repository = MemoryReservationRepository()
        self.completed_order_repository = MemoryCompletedOrderRepository()

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        pass


@pytest.fixture
def uow():
    return MemoryUnitOfWork()
