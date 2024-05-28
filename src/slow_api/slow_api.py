"""_summary_.

Raises:
    ValueError: _description_
    PathNotFoundException: _description_
    HttpMethodNotFoundException: _description_
    UnhandledProtocolException: _description_

Returns:
    _type_: _description_
"""

from __future__ import annotations

import logging
from asyncio import sleep
from typing import (
    Any,
    Awaitable,
    Callable,
    Literal,
    MutableMapping,
    Self,
)

Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Recieve = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
RouteHandler = Callable[[], bytes]


class UnhandledProtocolError(Exception):
    """UnhandledProtocolError."""

    ...


class PathNotFoundError(Exception):
    """UnhandledProtocolError."""

    ...


class HttpMethodNotFoundError(Exception):
    """HttpMethodNotFoundError."""

    ...


HttpMethod = Literal["GET", "POST"]


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

        self.routes[path][method] = handler

    def get(self: Self, path: str) -> Callable[[RouteHandler], RouteHandler]:
        """_summary_.

        Args:
            path (str): _description_
        """

        def _decorate(func: RouteHandler) -> RouteHandler:
            self.add_route(func, path, "GET")
            return func

        return _decorate

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

            if not message["more_body"]:
                break

        path = scope["path"]
        method = scope["method"]

        if path not in self.routes:
            raise PathNotFoundError

        if method not in self.routes[path]:
            raise HttpMethodNotFoundError

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
        # 123

        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        elif scope["type"] == "http":
            await self._handle_http(scope, receive, send)
        else:
            raise UnhandledProtocolError

        self.logger.info(f"End connection: {current_connection}")


if __name__ == "__main__":
    import uvicorn

    app = SlowAPI()

    @app.get("/")
    def get_index() -> bytes:
        """Index route returning "Hello World".

        Returns:
            bytes: Simply "Hello World".
        """
        return b"Hello World"

    @app.get("/items")
    def get_items() -> bytes:
        """A custom route.

        Returns:
            bytes: Simply "Here are some items"
        """
        return b"Here are some items"

    uvicorn.run(app, port=42069)
