import pandas as pd
from src.var import calculate_historical_var
import pytest

def test_historical_var() -> None:
    pnl: pd.Series = pd.Series([-10, -5, 0, 5, 10])

    result = calculate_historical_var(
        pnl,
        confidence_level=0.8,
        horizon_days=1,
    )

    assert result == pytest.approx(6.0)