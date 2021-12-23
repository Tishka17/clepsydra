import asyncio
from collections import Callable
from datetime import datetime
from logging import getLogger
from typing import Dict, Type, Optional, Tuple, Any, Sequence

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
        self.running_jobs = set()

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

    def _filter_not_running(self, jobs: Sequence[JobInfo]):
        return [job for job in jobs if job.job_id not in self.running_jobs]

    async def trigger_task(self, name, args, kwargs):
        task = self._get_task(name)
        context = self._new_context()
        await self.executor.execute(task, context, args, kwargs)

    async def _process_job(self, job: JobInfo, now: datetime):
        try:
            await self.trigger_task(
                name=job.name,
                args=job.args,
                kwargs=job.kwargs,
            )
        finally:
            self.running_jobs.remove(job.job_id)
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
            jobs = self._filter_not_running(jobs)
            logger.debug("Not running jobs: %s", jobs)
            if not jobs:
                logger.debug("No jobs, sleeping")
                await asyncio.sleep(1)
                continue
            for job in jobs:
                self.running_jobs.add(job.job_id)
                asyncio.create_task(self._process_job(job, now))
