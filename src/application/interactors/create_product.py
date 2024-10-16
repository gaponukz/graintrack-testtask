from src.application.dto import CreateProductInputDTO, CreateProductOutputDTO
from src.application.persistent import UnitOfWork
from src.application.usecases import CreateProductUseCase


class CreateProduct(CreateProductUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, product: CreateProductInputDTO) -> CreateProductOutputDTO:
        product_id = self._uow.product_repository.create(product)

        return CreateProductOutputDTO(product_id=product_id)
