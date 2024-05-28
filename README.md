# slow-api

![Tests](https://github.com/cooperellidge/slow-api/actions/workflows/tests.yml/badge.svg)

`SlowAPI` is a barebones, work-in-progress ASGI application framework inspired by `FastAPI`.
This project was created as an exercise to learn more about HTTP servers, web application frameworks, async Python, and Python packaging best practices.

> [!WARNING]
> This is obviously not production-ready... and is intended never to be.
> It is simply me playing around with ASGI implementations.

An upcoming little project of mine is to create other packages to fit into the ASGI stack including a protocol server (like `uvicorn`) and maybe a basic HTTP parser.

## Getting Started
1. Run `slow_api.py` as a Python script.
2. In another terminal, hit em with a curl
```bash
curl -v http://127.0.0.1:42069
```

## TODOs
- [x] connect uvicorn to slow-api
- [x] manage app startup/shutdown
- [x] return hello world
- [x] add routing
- [x] add some tests
- [x] improve type hinting, especially around endpoints and responses
- [x] include ruff, mypy
- [x] add dev scripts
- [x] add gh actions
- [ ] upload to test pypi
- [ ] investigate poetry, semver, gh actions to do CI/CD publishing to PyPI
- [ ] add all HTTP methods
- [ ] add different media types for responses, e.g. application/json
- [ ] add app logger with logger levels
- [ ] add websockets
- [ ] handle path params
- [ ] handle query params
- [ ] add custom lifespans (startup and shutdown events)
- [ ] add middleware
- [ ] add SwaggerUI docs, with type info
- [ ] add background tasks
- [ ] handle CORS config
