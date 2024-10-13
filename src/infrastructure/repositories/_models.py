from peewee import (
    DatabaseProxy,
    DoubleField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

db = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = db


class CategoryModel(BaseModel):
    class Meta:
        db_table = "categories"

    name = TextField()


class SubcategoryModel(BaseModel):
    class Meta:
        db_table = "subcategories"

    name = TextField()
    category = ForeignKeyField(CategoryModel)


class ProductModel(BaseModel):
    class Meta:
        db_table = "products"

    name = TextField()
    price = DoubleField()
    available = IntegerField()
    reserved = IntegerField()
    discount = IntegerField()
    subcategory = ForeignKeyField(SubcategoryModel)


class CustomerModel(BaseModel):
    class Meta:
        db_table = "customers"

    name = TextField()


class ReservationModel(BaseModel):
    class Meta:
        db_table = "reservations"
        primary_key = False
        indexes = (
            (
                (
                    "customer_id",
                    "product_id",
                ),
                True,
            ),
        )

    customer = ForeignKeyField(CustomerModel)
    product = ForeignKeyField(ProductModel)
    quantity = IntegerField()


class CompletedOrderModel(BaseModel):
    class Meta:
        db_table = "completed_orders"
        indexes = (
            (
                (
                    "customer_id",
                    "product_id",
                ),
                True,
            ),
        )

    customer = ForeignKeyField(CustomerModel)
    product = ForeignKeyField(ProductModel)
    quantity = IntegerField()
    total = DoubleField()
