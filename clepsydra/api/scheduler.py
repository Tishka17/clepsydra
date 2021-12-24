from __future__ import annotations

from typing import Protocol, Dict, Optional, Tuple, overload, Literal, Type, \
    Awaitable

from .context import (
    SyncH, SyncEH, AsyncEH, AsyncH, IsAsync,
)
from .rules import Rule


class Scheduler(Protocol[IsAsync]):
    @overload
    def task(self: Scheduler[Literal[True]],
             task_func: SyncH, *, name=None) -> SyncH:
        pass

    @overload
    def task(self: Scheduler[Literal[True]],
             task_func: SyncH, *, name=None) -> SyncH:
        pass

    @overload
    def error_handler(self: Scheduler[Literal[True]],
                      error_type: Type[Exception],
                      handler: AsyncEH) -> AsyncEH:
        ...

    @overload
    def error_handler(self: Scheduler[Literal[False]],
                      error_type: Type[Exception],
                      handler: SyncEH) -> SyncEH:
        ...

    @overload
    def middleware(self: Scheduler[Literal[True]],
                   middleware: AsyncH) -> AsyncH:
        ...

    @overload
    def middleware(self: Scheduler[Literal[False]],
                   middleware: SyncH) -> SyncH:
        ...

    @overload
    def add_job(
            self: Scheduler[Literal[True]],
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict] = None,
            meta: Optional[Dict] = None,
    ) -> Awaitable[str]:
        ...

    @overload
    def add_job(
            self: Scheduler[Literal[False]],
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict] = None,
            meta: Optional[Dict] = None,
    ) -> str:
        ...

    @overload
    def trigger_task(self: Scheduler[Literal[True]],
                     name: str, args, kwargs) -> Awaitable[None]:
        ...

    @overload
    def trigger_task(self: Scheduler[Literal[False]],
                     name: str, args, kwargs) -> None:
        ...

    @overload
    def run(self: Scheduler[Literal[True]]) -> Awaitable[None]:
        ...

    @overload
    def run(self: Scheduler[Literal[False]]) -> None:
        ...
