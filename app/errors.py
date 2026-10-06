class ApiError(Exception):
    status_code = 500


class UnauthorizedError(ApiError):
    status_code = 401


class NotFoundError(ApiError):
    status_code = 404


class ConflictError(ApiError):
    status_code = 409
