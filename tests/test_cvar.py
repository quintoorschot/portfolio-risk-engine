import pandas as pd
import numpy as np
from src.cvar import calculate_historical_cvar, calculate_parametric_cvar
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


# Test if the code correctly throws an error for invalid confidence levels
@pytest.mark.parametrize(
    "confidence_level",
    [-0.1, 0, 1, 1.1],
)
def test_historical_cvar_invalid_confidence_level(
    confidence_level: float,
) -> None:
    pnl: pd.Series = pd.Series([-25, -10, -5, 0, 10, 20])

    with pytest.raises(ValueError):
        calculate_historical_cvar(
            pnl,
            confidence_level=confidence_level,
            horizon_days=1,
        )


# Test if the code correctly throws an error for invalid horizon days values
@pytest.mark.parametrize(
        "horizon_days",
        [0, -1, -100, 0.5, 1.5]
)
def test_historical_cvar_invalid_horizon_days(
    horizon_days
) -> None:
    pnl: pd.Series = pd.Series([-25, -10, -5, 0, 10, 20])

    with pytest.raises(ValueError):
        calculate_historical_cvar(
            pnl,
            confidence_level=0.95,
            horizon_days=horizon_days,
        )


# ============== Parametric CVaR unit tests ============== #

def test_parametric_cvar_95_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([1, -1, 2, -2, 0])

    result: float = calculate_parametric_cvar(
        pnl,
        confidence_level=0.95,
        horizon_days=1,
    )

    assert result == pytest.approx(3.26166, rel=1e-4)

def test_parametric_cvar_all_zeros() -> None:
    pnl: pd.Series = pd.Series(np.zeros(10))

    result: float = calculate_parametric_cvar(
        pnl,
        confidence_level=0.95,
        horizon_days=1,
    )

    assert result == 0.0

def test_parametric_cvar_no_tail_losses() -> None:
    pnl: pd.Series = pd.Series([1, 2, 3, 4, 5])

    result: float = calculate_parametric_cvar(
        pnl,
        confidence_level=0.80,
        horizon_days=1,
    )

    assert result == 0.0

# Test if the code correctly throws an error for invalid confidence levels
@pytest.mark.parametrize(
    "confidence_level",
    [-0.1, 0, 1, 1.1],
)
def test_parametric_cvar_invalid_confidence_level(
    confidence_level: float,
) -> None:
    pnl: pd.Series = pd.Series([-25, -10, -5, 0, 10, 20])

    with pytest.raises(ValueError):
        calculate_parametric_cvar(
            pnl,
            confidence_level=confidence_level,
            horizon_days=1,
        )


# Test if the code correctly throws an error for invalid horizon days values
@pytest.mark.parametrize(
        "horizon_days",
        [0, -1, -100, 0.5, 1.5]
)
def test_parametric_cvar_invalid_horizon_days(
    horizon_days
) -> None:
    pnl: pd.Series = pd.Series([-25, -10, -5, 0, 10, 20])

    with pytest.raises(ValueError):
        calculate_parametric_cvar(
            pnl,
            confidence_level=0.95,
            horizon_days=horizon_days,
        )