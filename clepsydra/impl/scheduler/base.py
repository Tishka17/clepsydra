from datetime import datetime
from logging import getLogger
from typing import Dict, Type, Optional, Tuple, Any, TypeVar, Generic, Union, Callable

from clepsydra.api.context import Context
from clepsydra.api.exceptions import UnknownTaskError
from clepsydra.api.executor import Executor, AsyncExecutor
from clepsydra.api.rules import Rule
from clepsydra.api.scheduler import AsyncScheduler, Scheduler
from clepsydra.api.storage import Storage, JobInfo, AsyncStorage

logger = getLogger(__name__)

S = TypeVar("S", Storage, AsyncStorage)
E = TypeVar("E", Executor, AsyncExecutor)


class BaseScheduler(Generic[S, E]):
    def __init__(self, storage: S, executor: E):
        self.storage = storage
        self.executor = executor
        self.middlewares = []
        self.task_names: Dict[str, Callable] = {}
        self.error_handlers: Dict[Type, Callable] = {}
        self.running = True
        self.storage_limit = 100

    def task(self, task_func=None, *, name=None):
        if name is None:
            name = task_func.__name__
        if name in self.task_names:
            raise ValueError(f"Task with name {name} is already registered")
        self.task_names[name] = task_func

    def error_handler(self, error_type, handler):
        self.executor.error_handler(error_type, handler)

    def middleware(self, middleware):
        self.executor.middleware(middleware)

    def get_job(self, job_id: str):
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

    def _get_task(self, name):
        try:
            return self.task_names[name]
        except KeyError as e:
            raise UnknownTaskError from e

    def _new_context(self: Union[Scheduler, AsyncScheduler]):
        return Context(
            scheduler=self,
            data={},
            run_info={},
        )
