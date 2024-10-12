from application.usecases import DeleteProductUseCase
from src.application.persistent import UnitOfWork


class DeleteProduct(DeleteProductUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, product_id: int) -> None:
        self._uow.product_repository.delete(product_id)
