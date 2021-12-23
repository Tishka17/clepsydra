from clepsydra.api.scheduler import Scheduler, AsyncScheduler
from clepsydra.impl.executor.asyncio_executor import AsyncioExecutor
from clepsydra.impl.executor.sync_executor import SyncExecutor
from clepsydra.impl.scheduler.async_scheduler import AsyncSchedulerImpl
from clepsydra.impl.scheduler.sync_scheduler import SyncSchedulerImpl
from clepsydra.impl.storage.async_adapter import AsyncStorageAdapter
from clepsydra.impl.storage.memory_storage import MemoryStorage


def create_scheduler() -> Scheduler:
    return SyncSchedulerImpl(
        storage=MemoryStorage(),
        executor=SyncExecutor(),
    )


def create_async_scheduler() -> AsyncScheduler:
    return AsyncSchedulerImpl(
        storage=AsyncStorageAdapter(MemoryStorage()),
        executor=AsyncioExecutor(),
    )
