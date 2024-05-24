from asyncio import sleep
from typing import Any, Awaitable, Callable, MutableMapping


Scope = MutableMapping[str, Any]
Message = MutableMapping[str, Any]
Recieve = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]


class SlowAPI:

    connections = 0

    async def handle_lifespan(self, scope: Scope, receive: Recieve, send: Send):
        assert scope["type"] == "lifespan"

        while True:
            message = await receive()
            print(f"Message: {message}")

            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                break

    async def handle_http(self, scope: Scope, receive: Recieve, send: Send):
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

        response = {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")]
        }

        print(f"Sending response start: {response}")
        await send(response)

        response = {
            "type": "http.response.body",
            "body": b"Hello World",
            "more_body": False
        }

        print(f"Sending response body: {response}")
        await send(response)

    async def __call__(self, scope: Scope, receive: Recieve, send: Send) -> None:
        self.connections += 1
        current_connection = self.connections

        print(f"Begin connection: {current_connection}, Scope: {scope}")

        if scope["type"] == "lifespan":
            await self.handle_lifespan(scope, receive, send)
        if scope["type"] == "http":
            await self.handle_http(scope, receive, send)

        print(f"End connection: {current_connection}")


if __name__ == "__main__":
    import uvicorn

    app = SlowAPI()

    uvicorn.run(
        app,
        port=42069
    )
