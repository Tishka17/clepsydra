import asyncio
from collections import Callable
from datetime import datetime
from functools import partial
from logging import getLogger
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

    async def add_job(
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
        await self.storage.save_job(job)
        return job.job_id

    def _get_task(self, name):
        try:
            return self.task_names[name]
        except KeyError as e:
            raise UnknownTaskError from e

    def _new_context(self):
        return Context(
            scheduler=self,
            data={},
            run_info={},
        )

    async def trigger_task(self, name, args, kwargs):
        await self.executor.execute(
            self._get_task(name),
            self._new_context(),
            args, kwargs
        )

    async def _on_job_success(self, job: JobInfo, now: datetime):
        next_start = job.rule.get_next(now)
        if next_start:
            await self.storage.schedule_next(job.job_id, next_start)
        else:
            await self.storage.remove_job(job.job_id)

    async def run(self):
        while self.running:
            now = datetime.now()
            jobs = await self.storage.get_jobs(
                next_before=now,
                limit=self.storage_limit,
            )
            logger.debug("Read job from storage: %s", jobs)
            any_job_started = False
            for job in jobs:
                on_success = partial(self._on_job_success, job, now)
                job_started = await self.executor.execute(
                    self._get_task(job.name),
                    self._new_context(),
                    job.args, job.kwargs,
                    job_id=job.job_id,
                    on_job_success=on_success,
                )
                any_job_started = job_started or any_job_started

            if not any_job_started:
                logger.debug("No jobs started, sleeping")
                await asyncio.sleep(1)
