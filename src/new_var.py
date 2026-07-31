import pandas as pd

def calculate_historical_var(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:
    """Calculate the historical Value at Risk (VaR) for P&L data
    
    Uses historical P&L data to estimate the maximum expected loss at a given confidence level over the historical period.
    
    Args:
        connection: Active SQLite database connection containing historical price data.
        portfolio: Portfolio object containing assets and weights.
        confidence_level: Confidence level (0 < c < 1) for the calculation. Defaults to 0.95.

    Returns:
        The estimated maximum loss (>= 0.0) at the given confidence level.

    Raises:
        ValueError: If the confidence level is invalid or if there are insufficient historical returns to compute VaR.
    """

    if not 0 < confidence_level < 1:
        raise ValueError("[ERROR]: confidence level should be in a valid range (i.e. 0 < c < 1)!")

    value_at_risk: float = -float(daily_pnl.quantile(1 - confidence_level))
    value_at_risk = max(value_at_risk, 0.0)

    return value_at_risk