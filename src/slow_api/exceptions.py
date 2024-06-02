"""_summary_."""

from typing import Self

from slow_api.enums import HttpStatusCode

__all__ = (
    "HttpError",
    "UnhandledProtocolError",
    "PathNotFoundError",
    "MethodNotFoundError",
)


class HttpError(Exception):
    """HttpError."""

    def __init__(self: Self, status_code: HttpStatusCode, detail: str) -> None:
        """_summary_.

        Args:
            self (Self): _description_
            status_code (HttpStatusCode): _description_
            detail (str): _description_
        """
        self.status_code = status_code
        self.detail = detail


class UnhandledProtocolError(HttpError):
    """UnhandledProtocolError."""

    def __init__(self: Self) -> None:
        """_summary_.

        Args:
            self (Self): _description_
        """
        super().__init__(
            status_code=HttpStatusCode.HTTP_400_BAD,
            detail="Unhandled protocol",
        )


class PathNotFoundError(HttpError):
    """UnhandledProtocolError."""

    def __init__(self: Self) -> None:
        """_summary_.

        Args:
            self (Self): _description_
        """
        super().__init__(
            status_code=HttpStatusCode.HTTP_400_BAD, detail="Path not found"
        )


class MethodNotFoundError(HttpError):
    """MethodNotFoundError."""

    def __init__(self: Self) -> None:
        """_summary_.

        Args:
            self (Self): _description_
        """
        super().__init__(
            status_code=HttpStatusCode.HTTP_400_BAD, detail="Method not found"
        )
