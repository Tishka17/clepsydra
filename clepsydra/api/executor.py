from typing import Protocol, Callable, Type, Dict, List, Optional, Any


class Executor(Protocol):
    def error_handler(self, error_type, handler):
        pass

    def middleware(self, middleware):
        pass

    async def execute(
            self, task, context, args, kwargs,
            job_id: Optional[str] = None,
            on_job_success: Callable[[], Any] = None,
    ) -> bool:
        """
        Returns False if task was not started:
            if it already running, lack of resources and so on
        """
        pass


class BaseExecutor(Executor):
    def __init__(self):
        self.middlewares: List[Callable] = []
        self.error_handlers: Dict[Type, Callable] = {}
        self.running_jobs = set()

    def error_handler(self, error_type, handler):
        self.error_handlers[error_type] = handler

    def middleware(self, middleware):
        self.middlewares.append(middleware)

    def get_error_handler(self, exception: Exception) -> Optional[Callable]:
        for err_type in type(exception).mro():
            if err_type in self.error_handlers:
                return self.error_handlers[err_type]
        return

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
