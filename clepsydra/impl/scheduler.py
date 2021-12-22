from collections import Callable
from datetime import datetime
from logging import getLogger
from time import sleep
from typing import Dict, Type, Optional, Tuple, Any

from clepsydra import UnknownTaskError
from clepsydra.api.context import Context
from clepsydra.api.executor import Executor
from clepsydra.api.rules import Rule
from clepsydra.api.scheduler import Scheduler
from clepsydra.api.storage import Storage, JobInfo

logger = getLogger(__name__)


class SchedulerImpl(Scheduler):
    def __init__(self, storage: Storage, executor: Executor):
        self.storage = storage
        self.executor = executor
        self.middlewares = []
        self.task_names: Dict[str, Callable] = {}
        self.error_handlers: Dict[Type, Callable] = {}
        self.running = True

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

    def add_job(
            self,
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        now = datetime.now()
        next_start = rule.get_next(datetime.fromtimestamp(1))
        job = JobInfo(
            job_id=None,
            name=name,
            args=args or (),
            kwargs=kwargs or {},
            rule=rule,
            next_start=next_start,
            created_at=now,
            meta=meta,
        )
        self.storage.save_job(job)
        return job.job_id

    def trigger_task(self, name, args, kwargs):
        try:
            task = self.task_names[name]
        except KeyError as e:
            raise UnknownTaskError from e
        context = Context(
            scheduler=self,
            data={},
            run_info={},
        )
        self.executor.execute(task, context, args, kwargs)

    def run(self):
        while self.running:
            job = self.storage.get_next_job()
            logger.debug("Read job from sotrage: %s", job)
            if not job:
                logger.debug("No job, sleeping")
                sleep(1)
                continue
            now = datetime.now()
            if job.next_start > now:
                logger.debug("No early, sleeping")
                sleep(1)
                continue

            self.trigger_task(
                name=job.name,
                args=job.args,
                kwargs=job.kwargs,
            )
            next_start = job.rule.get_next(now)
            if next_start:
                self.storage.schedule_next(job.job_id, next_start)
            else:
                self.storage.remove_job(job.job_id)
