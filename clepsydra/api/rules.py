from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol, Optional


class Rule(Protocol):
    def get_next(self, after: datetime) -> Optional[datetime]:
        raise NotImplementedError


@dataclass
class IntervalRule(Rule):
    start: datetime
    period: timedelta

    def get_next(self, after: datetime) -> datetime:
        delta = after - self.start
        intervals = delta.total_seconds() // self.period.total_seconds() + 1
        return self.start + intervals * self.period


@dataclass
class SingleRun(Rule):
    when: datetime

    def get_next(self, after: datetime):
        if after > self.when:
            return None
        return self.when
