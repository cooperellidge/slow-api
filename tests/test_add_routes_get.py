from __future__ import annotations

import pytest
from slow_api import SlowAPI
from slow_api.enums import HttpMethod
from starlette.testclient import TestClient

app = SlowAPI()


@app.get("/decorated")
def _get_decorated() -> bytes:
    return b"Hello World"


def _get_not_decorated() -> bytes:
    return b"Hello World"


app.add_route(_get_not_decorated, "/not-decorated", HttpMethod.GET)

client = TestClient(app)


@pytest.mark.parametrize(
    "path,status_code,content",
    [
        ("/decorated", 200, b"Hello World"),
        ("/not-decorated", 200, b"Hello World"),
        ("/does-not-exist", 400, b"Path not found"),
    ],
)
def test_get(path: str, status_code: int, content: bytes | None) -> None:
    response = client.get(path)

    assert response.status_code == status_code
    assert response.content == content
