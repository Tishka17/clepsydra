from typing import Protocol

from .rules import Rule


class Scheduler(Protocol):
    def task(self, task_func=None, *, name=None):
        pass

    def error_handler(self, error_type, handler):
        pass

    def middleware(self, middleware):
        pass

    def add_task(self, name, rule: Rule, args=None, kwargs=None):
        pass

    def trigger_task(self, name, *args, **kwargs):
        pass

    def run(self):
        pass
