import logging
import time

from fastapi import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


async def logging_middleware(
    request: Request, call_next
) -> Response:

    start = time.perf_counter()

    logger.info("Incoming request %s %s", request.method, request.url.path)

    try:
        response = await call_next(request)

        process_time = time.perf_counter() - start

        logger.info(
            "Process timing %.4f seconds | Status code: %s",
            process_time,
            response.status_code,
        )

        response.headers["X-Process-Time"] = str(process_time)

        return response

    except Exception:
        logger.exception("Request failed: %s %s", request.method, request.url.path)
        raise
