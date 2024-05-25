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
