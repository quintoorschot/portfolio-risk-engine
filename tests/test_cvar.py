import pandas as pd
import numpy as np
from src.cvar import calculate_historical_cvar
import pytest

# ============== Historical CVaR unit tests ============== #

def test_historical_cvar_single_tail_loss() -> None:
    pnl: pd.Series = pd.Series([-10, -5, -2, 1, 3])

    result: float = calculate_historical_cvar(
        pnl,
        confidence_level=0.80,
        horizon_days=1,
    )

    # VaR threshold = 20th percentile = -6
    # Tail losses: [-10]
    # CVaR = 10
    assert result == pytest.approx(10.0)


def test_historical_cvar_multiple_tail_losses() -> None:
    pnl: pd.Series = pd.Series([-20, -10, -5, 0, 5])

    result: float = calculate_historical_cvar(
        pnl,
        confidence_level=0.60,
        horizon_days=1,
    )

    # VaR threshold = 40th percentile = -7.0
    # Tail losses: [-20, -10]
    # CVaR = -[(-20) + (-10)] / 2 = 15.0
    assert result == pytest.approx(15.0)


def test_historical_cvar_no_tail_losses() -> None:
    pnl: pd.Series = pd.Series([1, 2, 3, 4, 5])

    result: float = calculate_historical_cvar(
        pnl,
        confidence_level=0.80,
        horizon_days=1,
    )

    assert result == 0.0