from __future__ import annotations

import logging
from asyncio import sleep
from typing import (
    Any,
    Awaitable,
    Callable,
    MutableMapping,
    NoReturn,
    Self,
)

from slow_api.enums import HttpMethod
from slow_api.exceptions import (
    HttpError,
    MethodNotFoundError,
    PathNotFoundError,
    UnhandledProtocolError,
)

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Recieve = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
RouteHandler = Callable[[], bytes]


class SlowAPI:
    """SlowAPI."""

    def __init__(self: Self, logger: logging.Logger | None = None) -> None:
        """Init."""
        self.connections = 0
        self.routes: dict[str, Any] = {}
        self.logger = logging.getLogger() if logger is None else logger

    def add_route(
        self: Self,
        handler: RouteHandler,
        path: str,
        method: HttpMethod,
    ) -> None:
        """Adds a route to the app.

        Args:
            handler (RouteHandler): _description_
            path (str): _description_
            method (HttpMethod): _description_

        Raises:
            ValueError: _description_
        """
        if path not in self.routes:
            self.routes[path] = {}

        if method in self.routes[path]:
            raise ValueError("Method already added to route.")

        if method not in list(HttpMethod):
            raise NotImplementedError(f"{method} is not a valid HTTP method.")

        self.routes[path][method] = handler

    def get(self: Self, path: str) -> Callable[[RouteHandler], RouteHandler]:
        """_summary_.

        Args:
            path (str): _description_
        """

        def _decorate(func: RouteHandler) -> RouteHandler:
            self.add_route(func, path, HttpMethod.GET)
            return func

        return _decorate

    def post(self: Self, path: str) -> Callable[[RouteHandler], RouteHandler]:
        """_summary_.

        Args:
            path (str): _description_
        """

        def _decorate(func: RouteHandler) -> RouteHandler:
            self.add_route(func, path, HttpMethod.POST)
            return func

        return _decorate

    def _not_implemented(self: Self, _: str) -> None:
        raise NotImplementedError

    head = _not_implemented
    put = _not_implemented
    delete = _not_implemented
    connect = _not_implemented
    option = _not_implemented
    trace = _not_implemented
    patch = _not_implemented

    async def _handle_lifespan(
        self: Self,
        scope: Scope,
        receive: Recieve,
        send: Send,
    ) -> None:
        assert scope["type"] == "lifespan"

        while True:
            message = await receive()
            self.logger.debug(f"Message: {message}")

            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                break

    async def _handle_http(
        self: Self,
        scope: Scope,
        receive: Recieve,
        send: Send,
    ) -> None:
        assert scope["type"] == "http"

        # Remember, this is Slow API...
        await sleep(1)

        while True:
            message = await receive()
            self.logger.debug(f"Message: {message}")

            if message["type"] == "http.disconnect":
                return

            if "more_body" not in message or not message["more_body"]:
                break

        path = scope["path"]
        method = scope["method"]

        if path not in self.routes:
            raise PathNotFoundError

        if method not in self.routes[path]:
            raise MethodNotFoundError

        route = self.routes[path][method]

        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }

        self.logger.info(f"Sending response start: {response}")
        await send(response)

        body = route()

        response = {
            "type": "http.response.body",
            "body": body,
            "more_body": False,
        }

        self.logger.info(f"Sending response body: {response}")
        await send(response)

    async def _handle_http_error(
        self: Self, error: HttpError, send: Send
    ) -> None:
        response = {
            "type": "http.response.start",
            "status": error.status_code,
            "headers": [(b"content-type", b"text/plain")],
        }
        await send(response)

        response = {
            "type": "http.response.body",
            "body": error.detail.encode("utf-8"),
            "more_body": False,
        }
        await send(response)

    async def __call__(
        self: Self,
        scope: Scope,
        receive: Recieve,
        send: Send,
    ) -> None:
        """ASGI app callable interface.

        Args:
            self (Self): _description_
            scope (Scope): _description_
            receive (Recieve): _description_
            send (Send): _description_

        Raises:
            UnhandledProtocolError: _description_
        """
        self.connections += 1
        current_connection = self.connections

        self.logger.info(
            f"Begin connection: {current_connection}, Scope: {scope}"
        )

        # TODO(@cooperellidge): handle_websocket(...)
        # 1
        try:
            if scope["type"] == "lifespan":
                await self._handle_lifespan(scope, receive, send)
            elif scope["type"] == "http":
                await self._handle_http(scope, receive, send)
            else:
                raise UnhandledProtocolError
        except HttpError as e:
            self.logger.error(e)
            await self._handle_http_error(e, send)

        self.logger.info(f"End connection: {current_connection}")


def main() -> None:  # noqa: D103
    import uvicorn

    app = SlowAPI()

    @app.get("/")
    def get_index() -> bytes:
        return b"Hello World"

    @app.get("/items")
    def get_items() -> bytes:
        return b"Here are some items"

    uvicorn.run(app, port=42069)


if __name__ == "__main__":
    main()
