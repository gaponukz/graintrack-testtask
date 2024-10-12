from application.usecases import ReserveProductUseCase
from src.application.persistent import UnitOfWork
from src.domain.entities import SelectedProductItems


class ReserveProduct(ReserveProductUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, reservation: SelectedProductItems) -> None:
        with self._uow:
            product = self._uow.product_repository.get(
                reservation.product_id, for_update=True
            )

            product.reserve(reservation.quantity)

            self._uow.product_repository.update(product)
            self._uow.reservation_repository.create(reservation)
