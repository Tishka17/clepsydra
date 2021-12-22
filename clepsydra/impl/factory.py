from clepsydra.api.scheduler import Scheduler
from .asyncio_executor import AsyncioExecutor
from .memory_storage import MemoryStorage
from .scheduler import SchedulerImpl
from .sync_executor import SyncExecutor


def create_scheduler(sync_executor: bool = False) -> Scheduler:
    if sync_executor:
        executor = SyncExecutor()
    else:
        executor = AsyncioExecutor()
    return SchedulerImpl(
        storage=MemoryStorage(),
        executor=executor,
    )
