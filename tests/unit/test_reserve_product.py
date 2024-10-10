import pytest

from src.application.interactors.reserve_product import ReserveProduct
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
        reserved=0,
    )
    reservation = SelectedProductItems(customer_id, product_id, quantity=1)

    reserve_product = ReserveProduct(uow)
    reserve_product(reservation)

    product = uow.product_repository.get(product_id)

    assert product.available == 0
    assert product.reserved == 1
    assert uow.reservation_repository.get(customer_id, product_id) == reservation


def test_not_enough(uow):
    customer_id, product_id = 1, 1
    uow.product_repository.products[product_id] = Product(
        id=product_id,
        name="test",
        price=10,
        subcategory_id=1,
        available=1,
        reserved=3,
    )
    reservation = SelectedProductItems(customer_id, product_id, quantity=2)
    reserve_product = ReserveProduct(uow)

    with pytest.raises(ValidationError):
        reserve_product(reservation)

    product = uow.product_repository.get(product_id)

    assert product.available == 1
    assert product.reserved == 3
    assert (
        uow.reservation_repository.reservations.get((customer_id, product_id)) is None
    )
