from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from exceptions import DOPCApiError, OutOfRangeException, EmptyCartException
from routers import delivery

app = FastAPI()

app.include_router(delivery.router)


def create_exception_handler(
    status_code: int, initial_detail: str
) -> Callable[[Request, DOPCApiError], JSONResponse]:
    detail = {"message": initial_detail}

    async def exception_handler(_: Request, exc: DOPCApiError) -> JSONResponse:
        if exc.message:
            detail["message"] = exc.message
        if exc.name:
            detail["message"] = f"{detail['message']} [{exc.name}]"
        return JSONResponse(
            status_code=status_code, content={"detail": detail["message"]}
        )

    return exception_handler


app.add_exception_handler(
    exc_class_or_status_code=OutOfRangeException,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST,
        "We are sorry, this location is currently outside our delivery range."),
)

app.add_exception_handler(
    exc_class_or_status_code=EmptyCartException,
    handler=create_exception_handler(
        status.HTTP_400_BAD_REQUEST, "The cart is empty!"
    ),
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        _: Request, exc: RequestValidationError):
    missing_params = [
        param["loc"][1] for param in exc.errors() if param["type"] == "missing"
    ]
    invalid_venue = {
        param["input"] for param in exc.errors() if param["type"] == "literal_error"
    }

    error_messages = []
    if missing_params:
        error_messages.append(
            f"Missing query parameters: {
                ', '.join(missing_params)}"
            )
    if invalid_venue:
        error_messages.append(
            f"Invalid venue: {
                ", {invalid_venue}"}"
            )

    return JSONResponse(
        content={"detail": "; ".join(error_messages)},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
