import pandas as pd
import numpy as np
from src.var import calculate_historical_var, calculate_parametric_var
import pytest

# ============== Historical VaR unit tests ============== #

def test_historical_var_80_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([-10, -5, 0, 5, 10])

    result = calculate_historical_var(
        pnl,
        confidence_level=0.8,
        horizon_days=1,
    )

    # We use the Pandas percentile function with linear interpolation, so we can end up with values in-between actual PnL values.
    # 20th percentile = -6, therefore VaR = 6.
    assert result == pytest.approx(6.0)


def test_historical_var_95_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([-100, -50, -25, -10, -5, 0, 5, 10, 20, 30])

    result = calculate_historical_var(
        pnl,
        confidence_level=0.95,
        horizon_days=1,
    )

    assert result == pytest.approx(77.5)


def test_historical_var_all_zeros() -> None:
    pnl: pd.Series = pd.Series(np.zeros(10))

    result = calculate_historical_var(
        pnl,
        confidence_level=0.95,
        horizon_days=1
    )

    assert result == 0.0


# ============== Parametric VaR unit tests ============== #

def test_parametric_var_95_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([-2, -1, 0, 1, 2])

    result = calculate_parametric_var(
        pnl,
        confidence_level=0.95,
        horizon_days=1,
    )

    # Mean = 0
    # Sample std = sqrt(2.5) ≈ 1.5811
    # z_95 = Φ^{-1}(0.95) ≈ 1.64485
    #
    # VaR = 1.64485 * sqrt(2.5) ≈ 2.6016
    assert result == pytest.approx(2.6016, rel=1e-3)


def test_parametric_var_all_zeros() -> None:
    pnl: pd.Series = pd.Series(np.zeros(10))

    result = calculate_parametric_var(
        pnl,
        confidence_level=0.95,
        horizon_days=1,
    )

    assert result == 0.0