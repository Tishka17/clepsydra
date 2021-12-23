from typing import Protocol, Dict, Optional, Tuple

from .context import ErrorHandler, Handler, AsyncErrorHandler, AsyncHandler
from .rules import Rule


class Scheduler(Protocol):
    def task(self, task_func: Handler, *, name=None):
        pass

    def error_handler(self, error_type: Exception, handler: ErrorHandler):
        pass

    def middleware(self, middleware: Handler):
        pass

    def add_job(
            self,
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict] = None,
            meta: Optional[Dict] = None,
    ) -> str:
        pass

    def trigger_task(self, name, args, kwargs):
        pass

    def run(self):
        pass


class AsyncScheduler(Protocol):
    def task(self, task_func: AsyncHandler, *, name=None):
        pass

    def error_handler(self, error_type: Exception, handler: AsyncErrorHandler):
        pass

    def middleware(self, middleware: AsyncHandler):
        pass

    async def add_job(
            self,
            name: str,
            rule: Rule,
            args: Optional[Tuple] = None,
            kwargs: Optional[Dict] = None,
            meta: Optional[Dict] = None,
    ) -> str:
        pass

    async def trigger_task(self, name, args, kwargs):
        pass

    async def run(self):
        pass
