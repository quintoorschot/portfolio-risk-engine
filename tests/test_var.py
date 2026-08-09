import pandas as pd
from src.var import calculate_historical_var
import pytest

def test_historical_var_80_percent_confidence_1_day_horizon() -> None:
    pnl: pd.Series = pd.Series([-10, -5, 0, 5, 10])

    result = calculate_historical_var(
        pnl,
        confidence_level=0.8,
        horizon_days=1,
    )

    # We use the Pandas percentile function with interpolation, so we can end up with values in-between actual PnL values.
    # 20th percentile = -6, therefore VaR = 6.
    assert result == pytest.approx(6.0)