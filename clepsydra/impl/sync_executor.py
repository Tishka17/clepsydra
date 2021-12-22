from logging import getLogger

from clepsydra.api.executor import BaseExecutor

logger = getLogger(__name__)


class SyncExecutor(BaseExecutor):
    def execute(self, task, context, args, kwargs):
        try:
            for m in self.middlewares:
                m(context, *args, **kwargs)
            logger.debug("Run task: %s", task)
            task(context, *args, **kwargs)
        except Exception as e:
            for err_type in type(e).mro():
                if err_type in self.error_handlers:
                    self.error_handlers[err_type]()
                    return
            raise
