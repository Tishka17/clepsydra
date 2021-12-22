from typing import Protocol, Dict, Optional, Tuple

from .rules import Rule


class Scheduler(Protocol):
    def task(self, task_func=None, *, name=None):
        pass

    def error_handler(self, error_type, handler):
        pass

    def middleware(self, middleware):
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
