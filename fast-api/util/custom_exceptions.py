from fastapi import HTTPException, status, Request
from fastapi.responses import ORJSONResponse
from logging import Logger
from typing import Optional


class CustomException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
            self,
            message: Optional[str] = None,
            status_code: Optional[int] = None,
            logger: Optional[Logger] = None,
            *args, **kwargs
    ):
        if not status_code:
            status_code = self.status_code
        if logger:
            logger.error(str(message))

        super().__init__(status_code=status_code, detail=message, *args, **kwargs)


async def custom_exception_handler(
        request: Request,
        exc: CustomException
) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.status_code, content={'message': exc.detail})


class DatabaseException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
            self,
            message: Optional[str] = None,
            status_code: Optional[int] = None,
            logger: Optional[Logger] = None,
            *args, **kwargs
    ):
        if not status_code:
            status_code = self.status_code
        if logger:
            logger.error(str(message))

        super().__init__(status_code=status_code, detail=message, *args, **kwargs)


async def database_exception_handler(
        request: Request,
        exc: DatabaseException
) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.status_code, content={'message': exc.detail})


class AuthException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
            self,
            message: Optional[str] = None,
            status_code: Optional[int] = None,
            logger: Optional[Logger] = None,
            *args, **kwargs
    ):
        if not status_code:
            status_code = self.status_code
        if logger:
            logger.error(str(message))

        super().__init__(status_code=status_code, detail=message, *args, **kwargs)


async def auth_exception_handler(
        request: Request,
        exc: AuthException
) -> ORJSONResponse:
    return ORJSONResponse(status_code=exc.status_code, content={'message': exc.detail})
