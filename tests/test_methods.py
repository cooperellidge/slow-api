from typing import Callable

import pytest
from slow_api import SlowAPI
from slow_api.enums import HttpMethod
from starlette.testclient import TestClient

app = SlowAPI()


def route_builder(method: HttpMethod) -> Callable[[], bytes]:
    def route() -> bytes:
        return method.encode("utf-8")

    return route


@pytest.mark.parametrize(
    "method",
    [(HttpMethod.GET), (HttpMethod.POST)],
)
def test_implemented_http_methods(method: HttpMethod) -> None:
    app.add_route(route_builder(method), "/", method)

    client = TestClient(app)
    response = client.request(method=method, url="/")

    assert response.status_code == 200
    assert response.content == method.encode("utf-8")


@pytest.mark.parametrize(
    "method",
    [
        ("HEAD"),
        ("PUT"),
        ("DELETE"),
        ("CONNECT"),
        ("OPTIONS"),
        ("TRACE"),
        ("PATCH"),
    ],
)
def test_not_implemented_http_methods(method: HttpMethod) -> None:
    with pytest.raises(NotImplementedError):
        app.add_route(route_builder(method), "/", method)
