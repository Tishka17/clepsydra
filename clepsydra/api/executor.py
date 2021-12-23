from typing import (
    Protocol, Optional, Type, Tuple, Dict,
)

from .context import (
    Context, ErrorHandler, Handler, AsyncErrorHandler, AsyncHandler,
    OnSuccess, AsyncOnSuccess,
)


class Executor(Protocol):
    def error_handler(self,
                      error_type: Type[Exception],
                      handler: ErrorHandler) -> None:
        pass

    def middleware(self, middleware: Handler):
        pass

    def execute(
            self,
            task: Handler,
            context: Context,
            args: Tuple, kwargs: Dict,
            job_id: Optional[str] = None,
            on_job_success: Optional[OnSuccess] = None,
    ) -> bool:
        """
        Returns False if task was not started:
            if it already running, lack of resources and so on
        """
        pass


class AsyncExecutor(Protocol):
    def error_handler(self,
                      error_type: Type[Exception],
                      handler: AsyncErrorHandler) -> None:
        pass

    def middleware(self, middleware: AsyncHandler):
        pass

    async def execute(
            self,
            task: AsyncHandler,
            context: Context,
            args: Tuple, kwargs: Dict,
            job_id: Optional[str] = None,
            on_job_success: Optional[AsyncOnSuccess] = None,
    ) -> bool:
        """
        Returns False if task was not started:
            if it already running, lack of resources and so on
        """
        pass
