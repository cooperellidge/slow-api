from enum import IntEnum, StrEnum

__all__ = ("HttpStatusCode", "HttpMethod")


class HttpStatusCode(IntEnum):
    HTTP_200_GOOD = 200
    HTTP_400_BAD = 400


class HttpMethod(StrEnum):
    GET = "GET"
    POST = "POST"
