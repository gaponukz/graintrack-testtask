import pytest

from src.application.dto import CancelReservationInputDTO
from src.application.interactors.cancel_reservation import CancelReservation
from src.domain.entities import Product, SelectedProductItems
from src.domain.errors import ValidationError


def test(uow):
    customer_id, product_id = 1, 1
    uow.product_repository.products[product_id] = Product(
        id=product_id,
        name="test",
        price=10,
        subcategory_id=1,
        available=1,
        reserved=1,
    )

    uow.reservation_repository.create(
        SelectedProductItems(customer_id, product_id, quantity=1)
    )
    cancel_reservation = CancelReservation(uow)

    cancel_reservation(
        CancelReservationInputDTO(customer_id=customer_id, product_id=product_id)
    )

    product = uow.product_repository.get(product_id)

    assert product.available == 2
    assert product.reserved == 0
    assert (
        uow.reservation_repository.reservations.get((customer_id, product_id)) is None
    )


def test_not_enough(uow):
    customer_id, product_id = 1, 1
    uow.product_repository.products[product_id] = Product(
        id=product_id,
        name="test",
        price=10,
        subcategory_id=1,
        available=1,
        reserved=0,
    )

    uow.reservation_repository.create(
        SelectedProductItems(customer_id, product_id, quantity=1)
    )
    cancel_reservation = CancelReservation(uow)

    with pytest.raises(ValidationError):
        cancel_reservation(
            CancelReservationInputDTO(customer_id=customer_id, product_id=product_id)
        )

    product = uow.product_repository.get(product_id)

    assert product.available == 1
    assert product.reserved == 0
