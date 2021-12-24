from __future__ import annotations

from typing import (
    Protocol, Optional, Type, Tuple, Dict, overload, Literal, Awaitable,
)

from .context import (
    Context, AsyncH, AsyncEH, SyncH, SyncEH, Handler,
    OnSuccess, AsyncOnSuccess, IsAsync,
)


class Executor(Protocol[IsAsync]):
    @overload
    def error_handler(self: Executor[Literal[True]],
                      error_type: Type[Exception],
                      handler: AsyncEH) -> AsyncEH:
        ...

    @overload
    def error_handler(self: Executor[Literal[False]],
                      error_type: Type[Exception],
                      handler: SyncEH) -> SyncEH:
        ...

    @overload
    def middleware(self: Executor[Literal[True]],
                   middleware: AsyncH) -> AsyncH:
        ...

    @overload
    def middleware(self: Executor[Literal[False]],
                   middleware: SyncH) -> SyncH:
        ...

    @overload
    def execute(
            self: Executor[Literal[False]],
            task: Handler[False],
            context: Context,
            args: Tuple, kwargs: Dict,
            job_id: Optional[str] = None,
            on_job_success: Optional[OnSuccess] = None,
    ) -> bool:
        ...

    @overload
    def execute(
            self: Executor[Literal[True]],
            task: Handler[True],
            context: Context,
            args: Tuple, kwargs: Dict,
            job_id: Optional[str] = None,
            on_job_success: Optional[AsyncOnSuccess] = None,
    ) -> Awaitable[bool]:
        ...
