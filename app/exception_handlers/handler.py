import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    ApplicationAlreadyExistsException,
    InvalidApplicationStatusTransitionException,
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    JobNotFoundException,
    JobProfileNotFoundException,
    JobSeekerProfileAlreadyExistsException,
    NotAuthorizedException,
    UserNotFoundException,
)

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def invalid_refresh_token_handler(
        request: Request,
        exc: InvalidRefreshTokenException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobProfileNotFoundException)
    async def job_profile_not_found_handler(
        request: Request,
        exc: JobProfileNotFoundException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobSeekerProfileAlreadyExistsException)
    async def job_seeker_profile_already_exists_handler(
        request: Request,
        exc: JobSeekerProfileAlreadyExistsException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotAuthorizedException)
    async def not_authorized_handler(
        request: Request,
        exc: NotAuthorizedException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobNotFoundException)
    async def job_not_found_handler(request: Request, exc: JobNotFoundException):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )

    @app.exception_handler(ApplicationAlreadyExistsException)
    async def application_already_exists_handler(
        request: Request, exc: ApplicationAlreadyExistsException
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        logger.error("Exception handled: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidApplicationStatusTransitionException)
    async def invalid_application_status_handler(
        request: Request, exc: InvalidApplicationStatusTransitionException
    ):
        logger.error("Exception handled : %s ", exc)
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)}
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."},
        )
