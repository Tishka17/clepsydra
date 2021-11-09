from typing import Tuple, Callable, Any, Dict, Protocol

from .context import Context
from .scheduler import Scheduler


class Worker(Protocol):
    def process_task(
            self,
            scheduler: Scheduler,
            context: Context,
            task: Callable,
            args: Tuple, kwargs: Dict[str, Any]
    ):
        pass


class WorkerFactory(Protocol):
    def get_worker(self, timeout=None):
        pass
