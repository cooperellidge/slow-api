"""_summary_."""

from slow_api import SlowAPI


def test_add_index_route_with_decorator() -> None:
    """_summary_."""
    app = SlowAPI()

    @app.get("/")
    def get_index() -> bytes:
        return b"Hello World"

    assert "/" in app.routes
    assert "GET" in app.routes["/"]
    assert app.routes["/"]["GET"] == get_index


def test_add_index_route_with_method() -> None:
    """_summary_."""
    app = SlowAPI()

    def get_index() -> bytes:
        return b"Hello World"

    app.add_route(get_index, "/", "GET")

    assert "/" in app.routes
    assert "GET" in app.routes["/"]
    assert app.routes["/"]["GET"] == get_index
