from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Dict, Any, Callable, Awaitable, TypeVar, Literal, Protocol, overload,
)


@dataclass
class Context:
    scheduler: Any
    data: Dict[str, Any]
    run_info: Any


IsAsync = TypeVar("IsAsync", Literal[True], Literal[False], covariant=True)


class ErrorHandler(Protocol[IsAsync]):
    @overload
    def __call__(self: ErrorHandler[Literal[True]],
                 context: Context) -> None:
        ...

    @overload
    def __call__(self: ErrorHandler[Literal[False]],
                 context: Context) -> Awaitable[None]:
        ...


class Handler(Protocol[IsAsync]):
    @overload
    def __call__(self: Handler[Literal[True]],
                 context: Context, *args: Any, **kwargs: Any) -> Any:
        ...

    @overload
    def __call__(self: Handler[Literal[False]],
                 context: Context, *args: Any, **kwargs: Any) -> Awaitable:
        ...


class Middleware(Protocol[IsAsync]):
    @overload
    def __call__(self: Middleware[Literal[True]],
                 context: Context,
                 handler: Handler[Literal[True]],
                 *args: Any, **kwargs: Any) -> Any:
        ...

    @overload
    def __call__(self: Middleware[Literal[False]],
                 context: Context,
                 handler: Handler[Literal[False]],
                 *args: Any, **kwargs: Any) -> Awaitable:
        ...


OnSuccess = Callable[[], None]
AsyncOnSuccess = Callable[[], Awaitable[None]]

SyncH = TypeVar("SyncH", bound=Handler[Literal[False]])
AsyncH = TypeVar("AsyncH", bound=Handler[Literal[True]])
SyncEH = TypeVar("SyncEH", bound=ErrorHandler[Literal[False]])
AsyncEH = TypeVar("AsyncEH", bound=ErrorHandler[Literal[True]])
SyncM = TypeVar("SyncM", bound=Middleware[Literal[False]])
AsyncM = TypeVar("AsyncM", bound=Middleware[Literal[True]])
