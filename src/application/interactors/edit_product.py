from src.application.dto import EditProductInputDTO
from src.application.persistent import UnitOfWork
from src.application.usecases import EditProductUseCase


class EditProduct(EditProductUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: EditProductInputDTO) -> None:
        with self._uow:
            product = self._uow.product_repository.get(dto.product_id, for_update=True)

            if dto.price is not None:
                product.set_price(dto.price)

            if dto.discount is not None:
                product.set_discount(dto.discount)

            self._uow.product_repository.update(product)
