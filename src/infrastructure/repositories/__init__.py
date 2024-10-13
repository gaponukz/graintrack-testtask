from __future__ import annotations

from peewee import fn

from src.application.dto import (
    CreateProductInputDTO,
    GetProductsInputDTO,
    GetSellReportInputDTO,
    GetSellReportItem,
    GetSellReportOutputDTO,
)
from src.application.errors import ProductNotFoundError, ReservationNotFoundError
from src.application.persistent import (
    CompletedOrderRepository,
    ProductRepository,
    ReservationRepository,
    UnitOfWork,
)
from src.domain.entities import CompletedOrder, Product, SelectedProductItems
from src.infrastructure.repositories._models import (
    CategoryModel,
    CompletedOrderModel,
    ProductModel,
    ReservationModel,
    SubcategoryModel,
    db,
)


class SqlProductRepository(ProductRepository):
    def create(self, product: CreateProductInputDTO) -> int:
        return ProductModel.insert(
            name=product.name,
            price=product.price,
            available=product.available,
            subcategory=product.subcategory_id,
            reserved=0,
            discount=0,
        ).execute()

    def get_list(self, filters: GetProductsInputDTO) -> list[Product]:
        where = ProductModel.available > 0

        if filters.subcategory_id is not None:
            products = ProductModel.select()
            where &= ProductModel.subcategory == filters.subcategory_id

        elif filters.category_id:
            products = ProductModel.select().join(SubcategoryModel)
            where &= SubcategoryModel.category == filters.category_id

        else:
            products = ProductModel.select()

        return [
            self._from_model_to_entity(product) for product in products.where(where)
        ]

    def get(self, product_id: int, for_update: bool = False) -> Product:
        query = ProductModel.select().where(ProductModel.id == product_id)

        if for_update:
            query = query.for_update()

        try:
            model = query.get()

        except ProductModel.DoesNotExist:
            raise ProductNotFoundError(f"Can not get Product(id={product_id})")

        return self._from_model_to_entity(model)

    def update(self, product: Product):
        rows_updated = (
            ProductModel.update(
                {
                    ProductModel.price: product.price,
                    ProductModel.discount: product.discount,
                    ProductModel.available: product.available,
                    ProductModel.reserved: product.reserved,
                }
            )
            .where(ProductModel.id == product.id)
            .execute()
        )

        if rows_updated == 0:
            raise ProductNotFoundError(
                f"Can not update Product(id={product.id}): not found"
            )

    def delete(self, product_id: int):
        rows_removed = (
            ProductModel.delete().where(ProductModel.id == product_id).execute()
        )

        if rows_removed == 0:
            raise ProductNotFoundError(
                f"Can not delete Product(id={product_id}): not found"
            )

    def _from_model_to_entity(self, model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            price=model.price,
            subcategory_id=model.subcategory_id,
            available=model.available,
            reserved=model.reserved,
            discount=model.discount,
        )


class SqlReservationRepository(ReservationRepository):
    def create(self, reservation: SelectedProductItems):
        ReservationModel(
            customer=reservation.customer_id,
            product=reservation.product_id,
            quantity=reservation.quantity,
        ).save()

    def get(self, customer_id: int, product_id: int) -> SelectedProductItems:
        reservation = (
            ReservationModel.select()
            .where(
                ReservationModel.customer == customer_id,
                ReservationModel.product == product_id,
            )
            .first()
        )

        if reservation is None:
            raise ReservationNotFoundError(
                f"Reservation(customer_id={customer_id}, product_id={product_id}) not found"
            )

        return SelectedProductItems(
            customer_id=customer_id,
            product_id=product_id,
            quantity=reservation.quantity,
        )

    def delete(self, customer_id: int, product_id: int):
        rows_removed = (
            ReservationModel.delete()
            .where(
                ReservationModel.customer == customer_id,
                ReservationModel.product == product_id,
            )
            .execute()
        )

        if rows_removed == 0:
            raise ProductNotFoundError(
                f"Can not delete Product(id={product_id}): not found"
            )


class SqlCompletedOrderRepository(CompletedOrderRepository):
    def create(self, order: CompletedOrder):
        CompletedOrderModel.insert(
            customer=order.customer_id,
            product=order.product_id,
            quantity=order.quantity,
            total=order.total,
        ).execute()

    def get_sell_report(self, dto: GetSellReportInputDTO) -> GetSellReportOutputDTO:
        orders = (
            CompletedOrderModel.select(
                SubcategoryModel.name.alias("subcategory_name"),
                CategoryModel.name.alias("category_name"),
                fn.SUM(CompletedOrderModel.quantity).alias("quantity"),
                fn.SUM(CompletedOrderModel.total).alias("total"),
            )
            .join(ProductModel)
            .join(SubcategoryModel)
            .join(CategoryModel)
            .group_by(CategoryModel.id, SubcategoryModel.id)
            .limit(dto.limit)
            .offset(dto.offset)
            .objects()
        )

        if dto.subcategory_id is not None:
            orders = orders.where(SubcategoryModel.id == dto.subcategory_id)

        elif dto.category_id is not None:
            orders = orders.where(CategoryModel.id == dto.category_id)

        return GetSellReportOutputDTO(
            GetSellReportItem(
                category_name=item.category_name,
                subcategory_name=item.subcategory_name,
                quantity=item.quantity,
                total=item.total,
            )
            for item in orders
        )


class SqlUnitOfWork(UnitOfWork):
    def __init__(self):
        self._transaction = db.atomic()
        self._product_repository = SqlProductRepository()
        self._reservation_repository = SqlReservationRepository()
        self._completed_order_repository = SqlCompletedOrderRepository()

    def __enter__(self) -> SqlUnitOfWork:
        self._transaction.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._transaction.__exit__(exc_type, exc_value, traceback)

    @property
    def product_repository(self) -> ProductRepository:
        return self._product_repository

    @property
    def reservation_repository(self) -> ReservationRepository:
        return self._reservation_repository

    @property
    def completed_order_repository(self) -> CompletedOrderRepository:
        return self._completed_order_repository
