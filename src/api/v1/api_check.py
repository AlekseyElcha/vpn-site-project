from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK

router = APIRouter(prefix="/check", tags=["API Check"])


@router.get("/ping")
async def pong() -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_200_OK,
        content={
            "success": True
        }
    )
