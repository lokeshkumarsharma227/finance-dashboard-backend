from fastapi import HTTPException, status
# Custom HTTP exceptions with preset status codes.
# Services raise these — FastAPI automatically converts them to JSON error responses.
# Much cleaner than writing HTTPException(status_code=404, detail="...") everywhere.

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )