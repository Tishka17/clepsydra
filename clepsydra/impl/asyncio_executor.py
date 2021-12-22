from logging import getLogger

from clepsydra.api.executor import BaseExecutor

logger = getLogger(__name__)


class AsyncioExecutor(BaseExecutor):
    async def execute(self, task, context, args, kwargs):
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
