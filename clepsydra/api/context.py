from dataclasses import dataclass
from typing import Dict, Any, Callable, Awaitable


@dataclass
class Context:
    scheduler: Any
    data: Dict[str, Any]
    run_info: Any


ErrorHandler = Callable[[Exception, Context], None]
AsyncErrorHandler = Callable[[Exception, Context], Awaitable[None]]

Handler = Callable[..., None]
AsyncHandler = Callable[..., Awaitable[None]]
OnSuccess = Callable[[], None]
AsyncOnSuccess = Callable[[], Awaitable[None]]
