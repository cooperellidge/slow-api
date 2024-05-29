"""_summary_."""

import pytest
from slow_api import SlowAPI


@pytest.fixture(scope="function")
def decorated_app() -> SlowAPI:
    """_summary_.

    Returns:
        SlowAPI: _description_
    """
    app = SlowAPI()

    @app.get("/")
    def get_index() -> bytes:
        return b"Hello World"

    return app


@pytest.fixture(scope="function")
def app() -> SlowAPI:
    """_summary_.

    Returns:
        SlowAPI: _description_
    """
    app = SlowAPI()

    def get_index() -> bytes:
        return b"Hello World"

    app.add_route(get_index, "/", "GET")

    return app


def test_index_route_with_decorator(decorated_app: SlowAPI) -> None:
    """_summary_."""
    assert "/" in decorated_app.routes
    assert "GET" in decorated_app.routes["/"]
    assert decorated_app.routes["/"]["GET"]() == b"Hello World"


def test_index_route_with_method(app: SlowAPI) -> None:
    """_summary_."""
    assert "/" in app.routes
    assert "GET" in app.routes["/"]
    assert app.routes["/"]["GET"]() == b"Hello World"
