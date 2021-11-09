from dataclasses import dataclass
from typing import Dict, Any

from .scheduler import Scheduler


@dataclass
class Context:
    scheduler: Scheduler
    data: Dict[str, Any]
    run_info: Any
