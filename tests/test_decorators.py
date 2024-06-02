import pytest
from slow_api import SlowAPI
from slow_api.enums import HttpMethod


@pytest.fixture(scope="function")
def app() -> SlowAPI:
    app = SlowAPI()
    return app


def test_decorate_get(app: SlowAPI) -> None:
    @app.get("/")
    def index() -> bytes:
        return b"Hello World"

    assert "/" in app.routes
    assert HttpMethod.GET in app.routes["/"]
    assert app.routes["/"][HttpMethod.GET]() == b"Hello World"


def test_decorate_post(app: SlowAPI) -> None:
    @app.post("/")
    def index() -> bytes:
        return b"Hello World"

    assert "/" in app.routes
    assert HttpMethod.POST in app.routes["/"]
    assert app.routes["/"][HttpMethod.POST]() == b"Hello World"


def test_decorate_put(app: SlowAPI) -> None:
    with pytest.raises(NotImplementedError):

        @app.put("/")  # type: ignore[misc]
        def index() -> bytes:
            return b"Hello World"
