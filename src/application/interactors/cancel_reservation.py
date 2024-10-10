from src.application.dto import CancelReservationInputDTO
from src.application.persistent import UnitOfWork
from src.application.usercases import CancelReservationUseCase


class CancelReservation(CancelReservationUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: CancelReservationInputDTO) -> None:
        with self._uow:
            product = self._uow.product_repository.get(dto.product_id, for_update=True)
            reservation = self._uow.reservation_repository.get(
                customer_id=dto.customer_id,
                product_id=dto.product_id,
            )

            product.unreserve(reservation.quantity)

            self._uow.product_repository.update(product)
            self._uow.reservation_repository.delete(
                customer_id=reservation.customer_id,
                product_id=reservation.product_id,
            )
