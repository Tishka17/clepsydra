from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Tuple, Any, Optional, List, Dict, TypeVar, \
    Awaitable

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


AT = TypeVar("AT", None, Awaitable[None], covariant=True)


class BaseStorage(Protocol[AT]):
    def schedule_next(self, job_id: str, next_start: datetime) -> AT:
        raise NotImplementedError

    def mark_run_completed(self, job_id: str, started_at: datetime) -> AT:
        raise NotImplementedError

    def mark_started(self, job_id: str, started_at: datetime) -> AT:
        raise NotImplementedError

    def save_job(self, job: JobInfo) -> AT:
        raise NotImplementedError

    def remove_job(self, job_id: str) -> AT:
        raise NotImplementedError


class Storage(BaseStorage[None], Protocol):
    def get_next_job(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
    ) -> JobInfo:
        pass

    def get_jobs(
            self,
            next_after: Optional[datetime] = None,
            next_before: Optional[datetime] = None,
            limit: Optional[int] = None,
    ) -> List[JobInfo]:
        """
        Retrieves jobs with filtering in order of `next_start`
        """
        pass

    def get_job(self, job_id: str) -> JobInfo:
        pass


class AsyncStorage(BaseStorage[Awaitable[None]], Protocol):
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

    async def get_job(self, job_id: str) -> JobInfo:
        pass
