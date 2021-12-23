from datetime import datetime
from typing import Optional, List, Dict
from uuid import uuid4

from clepsydra.api.exceptions import JobNotFoundError
from clepsydra.api.storage import Storage, JobInfo


class MemoryStorage(Storage):
    def __init__(self):
        self.jobs: Dict[str, JobInfo] = {}

    def get_next_job(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> Optional[JobInfo]:
        jobs = self.get_jobs(next_after, next_before, limit=1)
        if not jobs:
            return None
        return jobs[0]

    def get_job(
            self, job_id: str,
    ) -> JobInfo:
        try:
            return self.jobs[job_id]
        except KeyError as e:
            raise JobNotFoundError from e

    def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
            limit: Optional[int] = None,
    ) -> List[JobInfo]:
        res: List[JobInfo] = []
        for job in self.jobs.values():
            if (
                    (next_after is None or job.next_start > next_after) and
                    (next_before is None or job.next_start < next_before)
            ):
                res.append(job)
        res.sort(key=lambda j: j.next_start)
        if limit is not None:
            res = res[:limit]
        return res

    def remove_job(self, job_id: str) -> None:
        del self.jobs[job_id]

    def schedule_next(self, job_id: str, next_start: datetime) -> None:
        self.jobs[job_id].next_start = next_start

    def mark_run_completed(self, job_id: str, started_at: datetime) -> None:
        pass

    def mark_started(self, job_id: str, started_at: datetime) -> None:
        pass

    def save_job(self, job: JobInfo) -> None:
        if job.job_id is None:
            job.job_id = uuid4().hex
        self.jobs[job.job_id] = job
