from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Tuple, Any, Optional, List

from .rules import Rule


@dataclass
class JobInfo:
    job_id: Optional[int]
    name: str
    args: Tuple[Any]
    kwargs: Tuple[Any]
    rule: Rule
    next_start: datetime
    created_at: datetime


class Storage(Protocol):
    def get_next_job(
            self,
            after: Optional[datetime] = None,
            before: Optional[datetime] = None,
    ) -> JobInfo:
        pass

    def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> List[JobInfo]:
        pass

    def schedule_next(self, job_id: int, next_start: datetime):
        pass

    def mark_completed(self, job_id: int):  # TODO what if not single run
        pass

    def mark_started(self, job_id: int):
        pass

    def save_task(self, job: JobInfo):
        pass
