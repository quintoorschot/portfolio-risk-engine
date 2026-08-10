from scipy.stats import norm
import pandas as pd
import numpy as np

def calculate_historical_var(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: Confidence level c ({confidence_level}) should be in a valid range (i.e. 0 < c < 1)!")

    if not isinstance(horizon_days, int) or horizon_days < 1:
        raise ValueError(f"[ERROR]: Horizon days ({horizon_days}) should be a postive integer")

    if len(daily_pnl) < horizon_days:
        raise ValueError(f"[ERROR]: Not enough observations to calculate historical VaR! The number of observations ({len(daily_pnl)}) should be larger than the value of horizon days ({horizon_days})!")

    horizon_pnl: pd.Series = daily_pnl.rolling(window=horizon_days).sum().dropna()

    value_at_risk: float = -float(horizon_pnl.quantile(1 - confidence_level))
    value_at_risk = max(value_at_risk, 0.0)

    return value_at_risk


def calculate_parametric_var(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:

    if not 0 < confidence_level < 1:
        raise ValueError(f"[ERROR]: Confidence level c ({confidence_level}) should be in a valid range (i.e. 0 < c < 1)!")

    if not isinstance(horizon_days, int) or horizon_days < 1:
        raise ValueError(f"[ERROR]: Horizon days ({horizon_days}) should be a postive integer")

    if daily_pnl.empty:
        raise ValueError(f"[ERROR] Not enough observations to calculate parametric VaR. PnL cannot be empty for parametric VaR calculations!")

    daily_pnl_mean: float = daily_pnl.mean()
    daily_pnl_volatility: float = daily_pnl.std()

    z_score: float = float(norm.ppf(confidence_level))

    value_at_risk: float = z_score * np.sqrt(horizon_days) * daily_pnl_volatility - daily_pnl_mean * horizon_days

    return value_at_risk