from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.exceptions import (
    InvalidCredentialsException,
    InvalidRefreshTokenException,
    JobNotFoundException,
    JobProfileNotFoundException,
    JobSeekerProfileAlreadyExistsException,
    NotAuthorizedException,
    UserNotFoundException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(
        request: Request,
        exc: InvalidCredentialsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidRefreshTokenException)
    async def invalid_refresh_token_handler(
        request: Request,
        exc: InvalidRefreshTokenException,
    ):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobProfileNotFoundException)
    async def job_profile_not_found_handler(
        request: Request,
        exc: JobProfileNotFoundException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobSeekerProfileAlreadyExistsException)
    async def job_seeker_profile_already_exists_handler(
        request: Request,
        exc: JobSeekerProfileAlreadyExistsException,
    ):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(NotAuthorizedException)
    async def not_authorized_handler(
        request: Request,
        exc: NotAuthorizedException,
    ):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": str(exc)},
        )

    @app.exception_handler(JobNotFoundException)
    async def job_not_found_handler(request: Request, exc: JobNotFoundException):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)}
        )
    
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(
        request: Request,
        exc: UserNotFoundException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )
