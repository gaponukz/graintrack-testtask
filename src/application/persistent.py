from __future__ import annotations

import typing

from src.application.dto import (
    CreateProductInputDTO,
    GetProductsInputDTO,
    GetSellReportInputDTO,
    GetSellReportOutputDTO,
)
from src.domain.entities import CompletedOrder, Product, SelectedProductItems


class ProductRepository(typing.Protocol):
    def create(self, product: CreateProductInputDTO) -> int: ...

    def get_list(self, filters: GetProductsInputDTO) -> list[Product]: ...

    def get(self, product_id: int, for_update: bool = False) -> Product: ...

    def update(self, product: Product): ...

    def delete(self, product_id: int): ...


class ReservationRepository(typing.Protocol):
    def create(self, reservation: SelectedProductItems): ...

    def get(self, customer_id: int, product_id: int) -> SelectedProductItems: ...

    def delete(self, customer_id: int, product_id: int): ...


class CompletedOrderRepository(typing.Protocol):
    def create(self, order: CompletedOrder): ...

    def get_sell_report(self, dto: GetSellReportInputDTO) -> GetSellReportOutputDTO: ...


class UnitOfWork(typing.Protocol):
    def __enter__(self) -> UnitOfWork: ...

    def __exit__(self, *args): ...

    @property
    def product_repository(self) -> ProductRepository: ...

    @property
    def reservation_repository(self) -> ReservationRepository: ...

    @property
    def completed_order_repository(self) -> CompletedOrderRepository: ...
