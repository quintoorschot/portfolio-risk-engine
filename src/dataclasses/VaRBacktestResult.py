from dataclasses import dataclass, field
from datetime import date
from typing import List
from decimal import Decimal

@dataclass
class VaRBacktestObservation:
    date: date
    value_at_risk: float
    actual_pnl: float
    exception: bool


@dataclass
class VaRBacktestSummary:
    observations: List[VaRBacktestObservation] = field(repr=False)
    confidence_level: float
    observation_count: int = field(init=False)
    exception_count: int = field(init=False)
    exception_rate: float = field(init=False)
    expected_exception_rate: Decimal = field(init=False)

    def __post_init__(self):
        self.observation_count = len(self.observations)
        self.exception_count = sum(observation.exception for observation in self.observations)
        self.exception_rate = self.exception_count / self.observation_count
        self.expected_exception_rate = Decimal("1") - Decimal(str(self.confidence_level))