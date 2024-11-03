from typing import Callable, Any

from fastapi import FastAPI

dependencies_list = list[
    tuple[
        Callable[..., Any],
        Callable[..., Any]
    ]
]
handlers_list = list[
    tuple[
        Any,
        Callable[..., Any]
    ]
]


def dependencies_init(
        app: FastAPI,
        deps: dependencies_list
) -> FastAPI:
    for dep in deps:
        app.dependency_overrides[dep[0]] = dep[1]

    return app


def exc_handlers_init(
    app: FastAPI,
    handlers: handlers_list
) -> FastAPI:
    for handler in handlers:
        app.exception_handlers[handler[0]] = handler[1]

    return app


def middlewares_init(
        app: FastAPI
):
    ...
