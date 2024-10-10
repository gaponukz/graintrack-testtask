import pytest

from src.domain.entities import CompletedOrder, Product, Reservation
from src.domain.errors import ValidationError


def test_product_ok():
    product = Product(
        id=1,
        name="test",
        price=10,
        subcategory_id=1,
        available=5,
        reserved=10,
        discount=50,
    )

    assert product.final_price == 5


@pytest.mark.parametrize(
    "fields",
    [
        dict(price=-1, available=5, reserved=10),
        dict(price=10, available=5, reserved=10, discount=101),
        dict(price=10, available=-1, reserved=10, discount=50),
        dict(price=10, available=5, reserved=-1, discount=50),
    ],
)
def test_product_invariant_violation(fields: dict):
    with pytest.raises(ValidationError):
        Product(id=1, name="test", subcategory_id=1, **fields)


def test_reservation():
    Reservation(customer_id=1, product_id=1, quantity=1)

    with pytest.raises(ValidationError):
        Reservation(customer_id=1, product_id=1, quantity=0)

    with pytest.raises(ValidationError):
        Reservation(customer_id=1, product_id=1, quantity=-1)


def test_completed_order():
    CompletedOrder(customer_id=1, product_id=1, quantity=1)

    with pytest.raises(ValidationError):
        CompletedOrder(customer_id=1, product_id=1, quantity=0)

    with pytest.raises(ValidationError):
        CompletedOrder(customer_id=1, product_id=1, quantity=-1)
