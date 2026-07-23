from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from backend_logging import logger

router = APIRouter(prefix="/check", tags=["API Check"])


@router.get("/ping")
async def pong() -> JSONResponse:
    logger.info("GET /ping request")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True
        }
    )
