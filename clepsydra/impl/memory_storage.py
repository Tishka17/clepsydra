from datetime import datetime
from typing import Optional, List, Dict
from uuid import uuid4

from clepsydra.api.storage import Storage, JobInfo


class MemoryStorage(Storage):
    def __init__(self):
        self.jobs: Dict[str, JobInfo] = {}

    def get_next_job(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> JobInfo:
        return min(
            self.get_jobs(next_after, next_before),
            key=lambda j: j.next_start
        )

    def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> List[JobInfo]:
        res: List[JobInfo] = []
        for job in self.jobs.values():
            if (
                    (next_after is None or job.next_start > next_after) and
                    (next_before is None or job.next_start < next_before)
            ):
                res.append(job)
        return res

    def schedule_next(self, job_id: str, next_start: datetime):
        self.jobs[job_id].next_start = next_start

    def mark_run_completed(self, job_id: str, started_at: datetime):
        pass

    def mark_started(self, job_id: str, started_at: datetime):
        pass

    def save_task(self, job: JobInfo):
        if job.job_id is None:
            job.job_id = uuid4().hex
        self.jobs[job.job_id] = job
