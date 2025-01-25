from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions import OutOfRangeException, EmptyCartException
from routers import delivery
from exceptions import format_all_validation_errors

app = FastAPI()

app.include_router(delivery.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        _: Request,
        exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=format_all_validation_errors(exc.errors())
    )


@app.exception_handler(OutOfRangeException)
async def out_of_range_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "We are sorry, this location is currently outside our delivery range."},
        headers={
            "X-Exception-Type": "OutOfRangeException"})


@app.exception_handler(EmptyCartException)
async def empty_cart_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "The cart is empty!"},
        headers={"X-Exception-Type": "EmptyCartException"}
    )
