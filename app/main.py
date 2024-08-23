import stripe
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app import settings
from app.api.router import router
from app.exceptions import NotFoundError, ValidationError


stripe.api_key = settings.STRIPE_API_KEY

app = FastAPI()

app.include_router(router)


@app.exception_handler(NotFoundError)
def not_found_error_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"code": 404, "message": exc.message},
    )


@app.exception_handler(ValidationError)
def validation_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"code": 400, "message": exc.message},
    )


@app.get("/health")
def home():
    return {"status": "ok"}
