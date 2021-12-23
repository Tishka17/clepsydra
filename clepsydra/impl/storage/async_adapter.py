from functools import partialmethod

from clepsydra.api.storage import Storage, AsyncStorage


class AsyncStorageAdapter(AsyncStorage):
    def __init__(self, storage: Storage):
        self.storage = storage

    async def _sync(self, *args, methodname, **kwargs):
        method = getattr(self.storage, methodname)
        return method(*args, **kwargs)

    get_next_job = partialmethod(_sync, methodname="get_next_job")  # type: ignore
    get_jobs = partialmethod(_sync, methodname="get_jobs")  # type: ignore
    get_job = partialmethod(_sync, methodname="get_job")  # type: ignore
    schedule_next = partialmethod(_sync, methodname="schedule_next")  # type: ignore
    mark_run_completed = partialmethod(_sync, methodname="mark_run_completed")  # type: ignore
    mark_started = partialmethod(_sync, methodname="mark_started")  # type: ignore
    save_job = partialmethod(_sync, methodname="save_job")  # type: ignore
    remove_job = partialmethod(_sync, methodname="remove_job")  # type: ignore
