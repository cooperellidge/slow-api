from asyncio import sleep
from typing import Any, Awaitable, Callable, Literal, MutableMapping


Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Recieve = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
RouteHandler = Callable[[], MutableMapping[str, Any]]


class UnhandledProtocolException(Exception):
    ...


class PathNotFoundException(Exception):
    ...


class HttpMethodNotFoundException(Exception):
    ...


HttpMethod = Literal[
    "GET", "POST"
]


class SlowAPI:

    connections = 0
    routes = {}

    def add_route(self, handler: RouteHandler, path: str, method: HttpMethod) -> None:
        print(handler, path, method)
        if path not in self.routes:
            self.routes[path] = {}

        if method in self.routes[path]:
            raise ValueError("Method already added to route.")

        self.routes[path][method] = handler

    def get(self, path: str):
        def decorate(func):
            self.add_route(func, path, "GET")
            return func
        return decorate

    async def _handle_lifespan(self, scope: Scope, receive: Recieve, send: Send) -> None:
        assert scope["type"] == "lifespan"

        while True:
            message = await receive()
            print(f"Message: {message}")

            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                break

    async def _handle_http(self, scope: Scope, receive: Recieve, send: Send) -> None:
        assert scope["type"] == "http"

        # Remember, this is Slow API...
        await sleep(1)

        while True:
            message = await receive()
            print(f"Message: {message}")

            if message["type"] == "http.disconnect":
                return

            if not message["more_body"]:
                break

        path = scope["path"]
        method = scope["method"]

        print(f"Routes: {self.routes}")

        if path not in self.routes:
            raise PathNotFoundException

        if method not in self.routes[path]:
            raise HttpMethodNotFoundException

        route = self.routes[path][method]

        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")]
        }

        print(f"Sending response start: {response}")
        await send(response)

        body = route()

        response = {
            "type": "http.response.body",
            "body": body,
            "more_body": False
        }

        print(f"Sending response body: {response}")
        await send(response)

    async def __call__(self, scope: Scope, receive: Recieve, send: Send) -> None:
        self.connections += 1
        current_connection = self.connections

        print(f"Begin connection: {current_connection}, Scope: {scope}")

        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        elif scope["type"] == "http":
            await self._handle_http(scope, receive, send)
        # elif scope["type"] == "http":
        # TODO: handle_websocket(...)
        else:
            raise UnhandledProtocolException

        print(f"End connection: {current_connection}")


if __name__ == "__main__":
    import uvicorn

    app = SlowAPI()

    @app.get("/")
    def get_index():
        return b"Hello World"

    @app.get("/items")
    def get_items():
        return b"Here are some items"

    uvicorn.run(
        app,
        port=42069
    )
