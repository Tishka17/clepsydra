import time
from datetime import datetime
from functools import partial
from logging import getLogger
from typing import Dict, Optional, Tuple, Any

from clepsydra.api.executor import Executor
from clepsydra.api.rules import Rule
from clepsydra.api.scheduler import Scheduler
from clepsydra.api.storage import JobInfo, Storage
from .base import BaseScheduler

logger = getLogger(__name__)


class SyncSchedulerImpl(BaseScheduler[Storage, Executor], Scheduler):
    def add_job(
            self,
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict[str, Any]] = None,
            meta: Optional[Dict[str, Any]] = None,
    ) -> str:
        job = self._job_info(
            name=name, rule=rule, args=args, kwargs=kwargs, meta=meta,
        )
        self.storage.save_job(job)
        return job.job_id

    def trigger_task(self, name, args, kwargs):
        self.executor.execute(
            self._get_task(name),
            self._new_context(),
            args, kwargs
        )

    def _on_job_success(self, job: JobInfo, now: datetime):
        next_start = job.rule.get_next(now)
        if next_start:
            self.storage.schedule_next(job.job_id, next_start)
        else:
            self.storage.remove_job(job.job_id)

    def run(self):
        while self.running:
            now = datetime.now()
            jobs = self.storage.get_jobs(
                next_before=now,
                limit=self.storage_limit,
            )
            logger.debug("Read job from storage: %s", jobs)
            any_job_started = False
            for job in jobs:
                on_success = partial(self._on_job_success, job, now)
                job_started = self.executor.execute(
                    self._get_task(job.name),
                    self._new_context(),
                    job.args, job.kwargs,
                    job_id=job.job_id,
                    on_job_success=on_success,
                )
                any_job_started = job_started or any_job_started

            if not any_job_started:
                logger.debug("No jobs started, sleeping")
                time.sleep(1)
