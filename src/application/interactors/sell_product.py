from application.usecases import SellProductUseCase
from src.application.persistent import UnitOfWork
from src.domain.entities import CompletedOrder, SelectedProductItems


class SellProduct(SellProductUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: SelectedProductItems) -> None:
        with self._uow:
            product = self._uow.product_repository.get(dto.product_id, for_update=True)

            product.sell(dto.quantity)

            self._uow.product_repository.update(product)
            self._uow.completed_order_repository.create(
                CompletedOrder(
                    customer_id=dto.customer_id,
                    product_id=dto.product_id,
                    quantity=dto.quantity,
                )
            )
