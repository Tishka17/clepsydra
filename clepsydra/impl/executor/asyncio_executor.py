import asyncio
from functools import partial
from logging import getLogger
from typing import Optional, Callable, Any

from clepsydra.api.executor import (
    AsyncHandler, AsyncErrorHandler, AsyncOnSuccess, AsyncExecutor,
)
from .base import BaseExecutor

logger = getLogger(__name__)


class AsyncioExecutor(BaseExecutor[AsyncHandler, AsyncErrorHandler],
                      AsyncExecutor):
    async def execute(
            self, task, context, args, kwargs,
            job_id: Optional[str] = None,
            on_job_success: Optional[AsyncOnSuccess] = None,
    ) -> bool:
        if self._is_job_running(job_id):
            return False
        self._add_running_job(job_id)
        func = partial(
            self._execute, task, context, args, kwargs,
            job_id=job_id, on_job_success=on_job_success,
        )
        asyncio.create_task(func())
        return True

    async def _execute(
            self, task, context, args, kwargs,
            job_id: Optional[str] = None,
            on_job_success: Callable[[], Any] = None,
    ):
        try:
            for m in self.middlewares:
                await m(context, *args, **kwargs)
            logger.debug("Run task: %s", task)
            await task(context, *args, **kwargs)
        except Exception as e:
            err_handler = self.get_error_handler(e)
            if not err_handler:
                raise
            await err_handler(e, context)
        finally:
            self._remove_running_job(job_id)
        if on_job_success:
            logger.debug("Calling on_job_success: %s", on_job_success)
            await on_job_success()
