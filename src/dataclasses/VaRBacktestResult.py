from dataclasses import dataclass, field
from scipy.stats import chi2
from datetime import date
from typing import List
from decimal import Decimal
import numpy as np

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


    def kupiec_test(self, confidence_level: float = 0.95) -> dict:

        n: int = self.observation_count
        x: int = self.exception_count

        expected_rate = 1 - self.confidence_level
        observed_rate = x / n

        log_likelihood_null = (
            x * np.log(expected_rate)
            + (n - x) * np.log(1 - expected_rate)
        )

        log_likelihood_alternative = 0.0

        if x > 0:
            log_likelihood_alternative += x * np.log(observed_rate)

        if x < n:
            log_likelihood_alternative += (
                (n - x) * np.log(1 - observed_rate)
            )

        lr_statistic = -2 * (
            log_likelihood_null - log_likelihood_alternative
        )

        p_value = chi2.sf(lr_statistic, df=1)

        return {
            "lr_statistic": lr_statistic,
            "p_value": p_value,
            "rejected": p_value < confidence_level,
        }