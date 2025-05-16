from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import organizations, buildings, activities
from app.core.utils import CustomException

app = FastAPI()

app.include_router(organizations.router, prefix="/api", tags=["organizations"])
app.include_router(buildings.router, prefix="/api", tags=["buildings"])
app.include_router(activities.router, prefix="/api", tags=["activities"])


@app.exception_handler(CustomException)
async def unicorn_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"details": exc.name}
    )
