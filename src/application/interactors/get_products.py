from application.usecases import GetProductsUseCase
from src.application.dto import GetProductsInputDTO
from src.application.persistent import UnitOfWork
from src.domain.entities import Product


class GetProducts(GetProductsUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, filters: GetProductsInputDTO) -> list[Product]:
        return self._uow.product_repository.get_list(filters)
