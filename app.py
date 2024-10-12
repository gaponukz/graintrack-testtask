import typing

from fastapi import Depends, FastAPI, Request, Response
from playhouse.postgres_ext import PostgresqlExtDatabase

import config
from src.application.dto import (
    CancelReservationInputDTO,
    CreateProductInputDTO,
    CreateProductOutputDTO,
    EditProductInputDTO,
    GetProductsInputDTO,
    GetSellReportInputDTO,
    GetSellReportItem,
)
from src.application.interactors.cancel_reservation import CancelReservation
from src.application.interactors.create_product import CreateProduct
from src.application.interactors.delete_product import DeleteProduct
from src.application.interactors.edit_product import EditProduct
from src.application.interactors.get_products import GetProducts
from src.application.interactors.get_sell_report import GetSellReport
from src.application.interactors.reserve_product import ReserveProduct
from src.application.interactors.sell_product import SellProduct
from src.application.usecases import (
    CancelReservationUseCase,
    CreateProductUseCase,
    DeleteProductUseCase,
    EditProductUseCase,
    GetProductsUseCase,
    GetSellReportUseCase,
    ReserveProductUseCase,
    SellProductUseCase,
)
from src.domain.entities import Product, SelectedProductItems
from src.infrastructure.controllers import ErrorHandlingMiddleware
from src.infrastructure.repositories import SqlUnitOfWork, db
from stub import Stub

app = FastAPI()
app.add_middleware(ErrorHandlingMiddleware)


@app.get("/products", response_model=list[Product])
def list_products(
    category_id: typing.Optional[int] = None,
    subcategory_id: typing.Optional[int] = None,
    get_products: GetProductsUseCase = Depends(Stub(GetProductsUseCase)),
):
    return get_products(GetProductsInputDTO(category_id, subcategory_id))


@app.post("/products", response_model=CreateProductOutputDTO)
def create_product(
    dto: CreateProductInputDTO,
    create_product: typing.Annotated[
        CreateProductUseCase, Depends(Stub(CreateProductUseCase))
    ],
):
    return create_product(dto)


@app.put("/products")
def update_product(
    dto: EditProductInputDTO,
    update_product: typing.Annotated[
        EditProductUseCase, Depends(Stub(EditProductUseCase))
    ],
):
    update_product(dto)
    return "OK"


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    delete_product: typing.Annotated[
        DeleteProductUseCase, Depends(Stub(DeleteProductUseCase))
    ],
):
    delete_product(product_id)
    return "OK"


@app.post("/products/reserve")
def make_reservation(
    dto: SelectedProductItems,
    reserve_product: typing.Annotated[
        ReserveProductUseCase, Depends(Stub(ReserveProductUseCase))
    ],
):
    reserve_product(dto)
    return "OK"


@app.post("/products/unreserve")
def make_unreservation(
    dto: CancelReservationInputDTO,
    unreserve_product: typing.Annotated[
        CancelReservationUseCase, Depends(Stub(CancelReservationUseCase))
    ],
):
    unreserve_product(dto)
    return "OK"


@app.post("/products/sell")
def sell_products(
    dto: SelectedProductItems,
    sell_products: typing.Annotated[
        SellProductUseCase, Depends(Stub(SellProductUseCase))
    ],
):
    sell_products(dto)
    return "OK"


@app.get("/products/sell/report", response_model=list[GetSellReportItem])
def get_sell_report(
    limit: int,
    offset: int,
    get_sell_report: typing.Annotated[
        GetSellReportUseCase, Depends(Stub(GetSellReportUseCase))
    ],
    category_id: typing.Optional[int] = None,
    subcategory_id: typing.Optional[int] = None,
):
    return get_sell_report(
        GetSellReportInputDTO(
            limit=limit,
            offset=offset,
            category_id=category_id,
            subcategory_id=subcategory_id,
        )
    )


db.initialize(PostgresqlExtDatabase(**config.DB_CONFIG))
uow = SqlUnitOfWork()

app.dependency_overrides = {
    GetProductsUseCase: lambda: GetProducts(uow),
    CreateProductUseCase: lambda: CreateProduct(uow),
    EditProductUseCase: lambda: EditProduct(uow),
    DeleteProductUseCase: lambda: DeleteProduct(uow),
    ReserveProductUseCase: lambda: ReserveProduct(uow),
    CancelReservationUseCase: lambda: CancelReservation(uow),
    SellProductUseCase: lambda: SellProduct(uow),
    GetSellReportUseCase: lambda: GetSellReport(uow),
}


@app.middleware("http")
def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        if db.is_closed():
            db.connect()

        response = call_next(request)

    finally:
        if not db.is_closed():
            db.close()

    return response
