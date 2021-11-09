from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union


@dataclass
class IntervalRule:
    start: datetime
    period: timedelta


OneTimeRule = datetime
Rule = Union[OneTimeRule, IntervalRule]
