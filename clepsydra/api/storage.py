from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Tuple, Any, Optional

from .rules import Rule


@dataclass
class JobInfo:
    job_id: Optional[int]
    name: str
    args: Tuple[Any]
    kwargs: Tuple[Any]
    rule: Rule
    next_start: datetime


class Storage(Protocol):
    def get_next_job(self) -> JobInfo:
        pass

    def schedule_next(self, job_id: int, next_start: datetime):
        pass

    def mark_completed(self, job_id: int):
        pass

    def save_task(self, job: JobInfo):
        pass
