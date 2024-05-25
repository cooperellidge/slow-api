# slow-api

This is obviously not production-ready... and is intended never to be.
It is simply me playing around with ASGI implementations.

`SlowAPI` is a barebones, work-in-progress ASGI application framework inspired by `FastAPI`.
This project was created as an exercise to learn more about HTTP servers, web application frameworks, and async Python.

An upcoming little project of mine is to create an ASGI protocol server, inspired by `uvicorn`, to parse the HTTP and hand over to apps made by this ASGI application framework, `SlowAPI`.

## Getting Started
1. Run `SlowAPI.py` as a Python script.
2. In another terminal, hit em with a curl
```bash
curl -v http://127.0.0.1:42069
```

## TODOs
- [] add all HTTP methods
- [] add some tests
- [] upload to test pypi
- [] add different media types for responses, e.g. application/json
- [] add app logger with logger levels
- [] add websockets
- [] handle path params dynamically
- [] improve type hinting, especially around endpoints and responses
- [] add lifespans (startup and shutdown events)
- [] add middleware
- [] add SwaggerUI docs
- [] add background tasks
- [] handle CORS config
