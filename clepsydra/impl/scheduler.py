from collections import Callable
from datetime import datetime
from time import sleep
from typing import Dict, Type

from clepsydra.api.context import Context
from clepsydra.api.rules import Rule
from clepsydra.api.scheduler import Scheduler
from clepsydra.api.storage import Storage, JobInfo
from clepsydra.impl.memory_storage import MemoryStorage


class SchedulerImpl(Scheduler):
    def __init__(self, storage: Storage):
        self.storage = storage
        self.middlewares = []
        self.task_names: Dict[str, Callable] = {}
        self.error_handlers: Dict[Type, Callable] = {}
        self.running = True

    def task(self, task_func=None, *, name=None):
        if name is None:
            name = task_func.__name__
        if name in self.task_names:
            raise ValueError(f"Task with name {name} is already registered")

    def error_handler(self, error_type, handler):
        self.error_handlers[error_type] = handler

    def middleware(self, middleware):
        self.middlewares.append(middleware)

    def add_job(self, name, rule: Rule, args=None, kwargs=None):
        now = datetime.now()
        next_start = rule.get_next(now)
        job = JobInfo(
            job_id=None,
            name=name,
            args=args,
            kwargs=kwargs,
            rule=rule,
            next_start=next_start,
            created_at=now,
        )
        self.storage.save_task(job)

    def trigger_task(self, name, args, kwargs):
        task = self.task_names[name]
        data = {}
        context = Context(
            scheduler=self,
            data=data,
            run_info={},
        )
        try:
            for m in self.middlewares:
                m(context, *args, **kwargs)
            task(context, *args, **kwargs)
        except Exception as e:
            for err_type in type(e).mro():
                if err_type in self.error_handlers:
                    self.error_handlers[err_type]()
                    return

    def run(self):
        while self.running:
            job = self.storage.get_next_job()
            if not job:
                sleep(1)
                continue
            now = datetime.now()
            if job.next_start > now:
                sleep(1)
                continue

            self.trigger_task(
                name=job.name,
                args=job.args,
                kwargs=job.kwargs,
            )
            next_start = job.rule.get_next(now)
            self.storage.schedule_next(job.job_id, next_start)


def create_scheduler() -> Scheduler:
    return SchedulerImpl(
        storage=MemoryStorage(),
    )
