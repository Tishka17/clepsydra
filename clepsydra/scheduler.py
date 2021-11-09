from .api.scheduler import Scheduler


class SchedulerImpl(Scheduler):
    pass


def create_scheduler() -> Scheduler:
    return SchedulerImpl()
