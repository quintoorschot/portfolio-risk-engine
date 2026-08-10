import pandas as pd
import numpy as np
from src.cvar import calculate_historical_cvar
import pytest

# ============== Historical CVaR unit tests ============== #

def test_historical_cvar_80_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([-10, -5, -2, 1, 3])

    result: float = calculate_historical_cvar(
        pnl,
        confidence_level=0.80,
        horizon_days=1,
    )

    assert result == pytest.approx(10.0)