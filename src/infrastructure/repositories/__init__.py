from __future__ import annotations

from src.application.dto import CreateProductInputDTO, GetProductsInputDTO
from src.application.persistent import (
    CompletedOrderRepository,
    ProductRepository,
    ReservationRepository,
    UnitOfWork,
)
from src.domain.entities import CompletedOrder, Product, SelectedProductItems


class SqlProductRepository(ProductRepository):
    def create(self, product: CreateProductInputDTO) -> int:
        raise NotImplementedError

    def get_list(self, filters: GetProductsInputDTO) -> list[Product]:
        raise NotImplementedError

    def get(self, product_id: int, for_update: bool = False) -> Product:
        raise NotImplementedError

    def update(self, product: Product):
        raise NotImplementedError

    def delete(self, product_id: int):
        raise NotImplementedError


class SqlReservationRepository(ReservationRepository):
    def create(self, reservation: SelectedProductItems):
        raise NotImplementedError

    def get(self, customer_id: int, product_id: int) -> SelectedProductItems:
        raise NotImplementedError

    def delete(self, customer_id: int, product_id: int):
        raise NotImplementedError


class SqlCompletedOrderRepository(CompletedOrderRepository):
    def create(self, order: CompletedOrder):
        raise NotImplementedError


class SqlUnitOfWork(UnitOfWork):
    def __enter__(self) -> SqlUnitOfWork:
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, traceback):
        raise NotImplementedError

    @property
    def product_repository(self) -> ProductRepository:
        raise NotImplementedError

    @property
    def reservation_repository(self) -> ReservationRepository:
        raise NotImplementedError

    @property
    def completed_order_repository(self) -> CompletedOrderRepository:
        raise NotImplementedError
