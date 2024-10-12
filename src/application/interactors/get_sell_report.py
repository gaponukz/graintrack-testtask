from application.usecases import GetSellReportUseCase
from src.application.dto import GetSellReportInputDTO, GetSellReportOutputDTO
from src.application.persistent import UnitOfWork


class GetSellReport(GetSellReportUseCase):
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def __call__(self, dto: GetSellReportInputDTO) -> GetSellReportOutputDTO:
        return self._uow.completed_order_repository.get_sell_report(dto)
