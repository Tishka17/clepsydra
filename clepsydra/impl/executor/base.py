from typing import Optional, List, Dict, Type, Generic

from clepsydra.api.context import (
    H, EH,
)


class BaseExecutor(Generic[H, EH]):
    def __init__(self):
        self.middlewares: List[H] = []
        self.error_handlers: Dict[Type, EH] = {}
        self.running_jobs = set()

    def error_handler(self, error_type: Type[Exception], handler: EH):
        self.error_handlers[error_type] = handler

    def middleware(self, middleware: H):
        self.middlewares.append(middleware)

    def get_error_handler(self, exception: Exception) -> Optional[EH]:
        for err_type in type(exception).mro():
            if err_type in self.error_handlers:
                return self.error_handlers[err_type]
        return None

    def _add_running_job(self, job_id: Optional[str]) -> None:
        if job_id is None:
            return
        self.running_jobs.add(job_id)

    def _remove_running_job(self, job_id: Optional[str]) -> None:
        if job_id is None:
            return
        self.running_jobs.remove(job_id)

    def _is_job_running(self, job_id: Optional[str]) -> bool:
        if job_id is None:
            return False
        return job_id in self.running_jobs
