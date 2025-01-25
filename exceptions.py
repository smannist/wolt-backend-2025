from fastapi import HTTPException


class DOPCApiError(HTTPException):
    def __init__(self, status_code: int, message: str, name: str = None):
        self.status_code = status_code
        self.message = message
        self.name = name
        super().__init__(status_code=status_code, detail=message)


class OutOfRangeException(DOPCApiError):
    pass


class EmptyCartException(DOPCApiError):
    pass
