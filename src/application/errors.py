class ApplicationError(Exception):
    pass


class NotFoundError(ApplicationError):
    pass


class ProductNotFoundError(NotFoundError):
    pass


class ReservationNotFoundError(NotFoundError):
    pass
