from __future__ import annotations

from datetime import datetime
from logging import getLogger
from typing import (
    Dict, Type, Optional, Tuple, Any, TypeVar, Generic, Union, List, Literal,
    overload,
)

from clepsydra.api.context import (
    Context, Handler, H, EH
)
from clepsydra.api.exceptions import UnknownTaskError
from clepsydra.api.executor import Executor, AsyncExecutor
from clepsydra.api.rules import Rule
from clepsydra.api.scheduler import AsyncScheduler, Scheduler
from clepsydra.api.storage import Storage, JobInfo, AsyncStorage

logger = getLogger(__name__)

S = TypeVar("S", Storage, AsyncStorage)
E = TypeVar("E", Executor, AsyncExecutor)

IsAsync = TypeVar("IsAsync", Literal[True], Literal[False])


class BaseScheduler(Generic[IsAsync]):
    @overload
    def __init__(self: BaseScheduler[True],
                 storage: AsyncStorage, executor: AsyncExecutor) -> None:
        ...

    def __init__(self: BaseScheduler[False], storage: S, executor: E) -> None:
        self.storage: S = storage
        self.executor: E = executor
        self.middlewares: List[H] = []
        self.task_names: Dict[str, H] = {}
        self.error_handlers: Dict[Type, EH] = {}
        self.running = True
        self.storage_limit = 100

    def task(self, task_func: H, *, name=None) -> H:
        if name is None:
            name = task_func.__name__
        if name in self.task_names:
            raise ValueError(f"Task with name {name} is already registered")
        self.task_names[name] = task_func
        return task_func

    def error_handler(self, error_type: Type[Exception], handler: EH) -> EH:
        return self.executor.error_handler(error_type, handler)

    def middleware(self, middleware: H) -> H:
        return self.executor.middleware(middleware)

    def get_job(self, job_id: str) -> JobInfo:
        return self.storage.get_job(job_id)

    def _job_info(
            self,
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            meta: Optional[Dict[str, Any]] = None,
    ) -> JobInfo:
        now = datetime.now()
        next_start = rule.get_next(datetime.fromtimestamp(1))
        return JobInfo(
            job_id=None,
            name=name,
            args=args or (),
            kwargs=kwargs or {},
            rule=rule,
            next_start=next_start,
            created_at=now,
            meta=meta,
        )

    def _get_task(self, name) -> Handler:
        try:
            return self.task_names[name]
        except KeyError as e:
            raise UnknownTaskError from e

    def _new_context(self: Union[Scheduler, AsyncScheduler]) -> Context:
        return Context(
            scheduler=self,
            data={},
            run_info={},
        )
