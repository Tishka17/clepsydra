from concurrent.futures import ThreadPoolExecutor, Executor
from functools import partial
from logging import getLogger
from typing import Optional, Callable, Any

from clepsydra.api.executor import BaseExecutor

logger = getLogger(__name__)


class SyncExecutor(BaseExecutor):
    def __init__(self, executor: Executor = None):
        super().__init__()
        self.executor = executor or ThreadPoolExecutor()

    def execute(
            self, task, context, args, kwargs,
            job_id: Optional[str] = None,
            on_job_success: Callable[[], Any] = None,
    ) -> bool:
        if self._is_job_running(job_id):
            return False
        self._add_running_job(job_id)

        func = partial(self._execute, task, context, args, kwargs)
        self.executor.submit(func)
        return True

    def _execute(
            self, task, context, args, kwargs,
            job_id: Optional[str] = None,
            on_job_success: Callable[[], Any] = None,
    ):
        try:
            for m in self.middlewares:
                m(context, *args, **kwargs)
            logger.debug("Run task: %s", task)
            task(context, *args, **kwargs)
        except Exception as e:
            err_handler = self.get_error_handler(e)
            if not err_handler:
                raise
            err_handler(e, context)
        finally:
            self._remove_running_job(job_id)
        if on_job_success:
            on_job_success()
