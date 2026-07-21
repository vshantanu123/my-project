from fastapi import Request, status
from fastapi.exception_handlers import request_validation_exception_handler, http_exception_handler
from fastapi.exceptions import HTTPException as StarletteHTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app import app as fastapi_app


class ApplicationException(Exception):
    status_code: int
    detail = None

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


@fastapi_app.exception_handler(ApplicationException)
async def custom_exception_handler(request: Request, exc: ApplicationException):
    return JSONResponse(
        status_code=status.exc.status_code,
        content={"success": False, "error_code": exc.status_code, "message": exc.detail},
    )


@fastapi_app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, exc):
    """

    :param request:
    :param exc:
    :return:
    """
    return await request_validation_exception_handler(request, exc)


@fastapi_app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    :param request:
    :param exc:
    :return:
    """
    return await http_exception_handler(request, exc)


@fastapi_app.exception_handler(Exception)
async def global_unhandled_exception_handler(request: Request, exc: Exception):
    # Place production logger here (e.g., logging.exception(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False,
                 "error_code": "INTERNAL_SERVER_ERROR",
                 "message": "An unexpected error occurred."},
    )
