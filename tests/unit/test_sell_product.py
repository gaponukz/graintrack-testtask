import pytest

from src.application.interactors.sell_product import SellProduct
from src.domain.entities import CompletedOrder, Product, SelectedProductItems
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

    sell_product = SellProduct(uow)

    sell_product(
        SelectedProductItems(customer_id=customer_id, product_id=product_id, quantity=1)
    )

    product = uow.product_repository.get(product_id)

    assert product.available == 0
    assert product.reserved == 1
    assert uow.completed_order_repository.orders[0] == CompletedOrder(
        customer_id=1,
        product_id=1,
        quantity=1,
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

    sell_product = SellProduct(uow)

    with pytest.raises(ValidationError):
        sell_product(
            SelectedProductItems(
                customer_id=customer_id, product_id=product_id, quantity=2
            )
        )

    product = uow.product_repository.get(product_id)

    assert product.available == 1
    assert product.reserved == 0
    assert uow.completed_order_repository.orders == []
