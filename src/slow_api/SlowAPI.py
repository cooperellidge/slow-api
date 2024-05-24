class SlowAPI:

    connections = 0

    async def __call__(self, scope, send, receive) -> None:
        self.connections += 1
        current_connection = self.connections

        print(f"Begin connection: {current_connection}")
        print(f"Scope: {scope}")
        print(f"End connection: {current_connection}")


if __name__ == "__main__":
    import uvicorn

    app = SlowAPI()

    uvicorn.run(
        app,
        port=42069
    )
