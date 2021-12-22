from clepsydra.api.scheduler import Scheduler
from .memory_storage import MemoryStorage
from .scheduler import SchedulerImpl
from .sync_executor import SyncExecutor


def create_scheduler() -> Scheduler:
    return SchedulerImpl(
        storage=MemoryStorage(),
        executor=SyncExecutor(),
    )
