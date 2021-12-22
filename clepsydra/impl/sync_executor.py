import asyncio
from functools import partial
from logging import getLogger

from clepsydra.api.executor import BaseExecutor

logger = getLogger(__name__)


class SyncExecutor(BaseExecutor):
    def __init__(self, executor=None):
        super().__init__()
        self.executor = executor

    async def execute(self, task, context, args, kwargs):
        loop = asyncio.get_running_loop()
        func = partial(self._execute, task, context, args, kwargs)
        await loop.run_in_executor(self.executor, func)

    def _execute(self, task, context, args, kwargs):
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
