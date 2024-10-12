from src.application import UseCase
from src.application.dto import (
    CancelReservationInputDTO,
    CreateProductInputDTO,
    CreateProductOutputDTO,
    EditProductInputDTO,
    GetProductsInputDTO,
    GetSellReportInputDTO,
    GetSellReportOutputDTO,
)
from src.domain.entities import Product, SelectedProductItems


class GetProductsUseCase(UseCase[GetProductsInputDTO, list[Product]]):
    pass


class CreateProductUseCase(UseCase[CreateProductInputDTO, CreateProductOutputDTO]):
    pass


class EditProductUseCase(UseCase[EditProductInputDTO, None]):
    pass


class DeleteProductUseCase(UseCase[int, None]):
    pass


class ReserveProductUseCase(UseCase[SelectedProductItems, None]):
    pass


class CancelReservationUseCase(UseCase[CancelReservationInputDTO, None]):
    pass


class SellProductUseCase(UseCase[SelectedProductItems, None]):
    pass


class GetSellReportUseCase(UseCase[GetSellReportInputDTO, GetSellReportOutputDTO]):
    pass
