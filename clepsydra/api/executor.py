from typing import Protocol, Callable, Type, Dict, List, Optional


class Executor(Protocol):
    def error_handler(self, error_type, handler):
        pass

    def middleware(self, middleware):
        pass

    async def execute(self, task, context, args, kwargs):
        pass


class BaseExecutor(Executor):
    def __init__(self):
        self.middlewares: List[Callable] = []
        self.error_handlers: Dict[Type, Callable] = {}

    def error_handler(self, error_type, handler):
        self.error_handlers[error_type] = handler

    def middleware(self, middleware):
        self.middlewares.append(middleware)

    def get_error_handler(self, exception: Exception) -> Optional[Callable]:
        for err_type in type(exception).mro():
            if err_type in self.error_handlers:
                return self.error_handlers[err_type]
        return
