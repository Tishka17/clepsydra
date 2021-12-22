from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Tuple, Any, Optional, List, Dict

from .rules import Rule


@dataclass
class JobInfo:
    job_id: Optional[str]
    name: str
    args: Tuple[Any]
    kwargs: Dict[str, Any]
    rule: Rule
    next_start: datetime
    created_at: datetime
    meta: Optional[Dict[str, Any]]


class Storage(Protocol):
    async def get_next_job(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> JobInfo:
        pass

    async def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
            limit: Optional[int] = None,
    ) -> List[JobInfo]:
        """
        Retrieves jobs with filtering in order of `next_start`
        """
        pass

    async def get_job(
            self, job_id: str,
    ) -> JobInfo:
        pass

    async def schedule_next(self, job_id: str, next_start: datetime):
        pass

    async def mark_run_completed(self, job_id: str, started_at: datetime):
        pass

    async def mark_started(self, job_id: str, started_at: datetime):
        pass

    async def save_job(self, job: JobInfo):
        pass

    async def remove_job(self, job_id: str):
        pass
