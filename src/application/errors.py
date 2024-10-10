class ApplicationError(Exception):
    pass


class ProductNotFoundError(ApplicationError):
    pass


class ReservationNotFoundError(ApplicationError):
    pass
