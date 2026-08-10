import pandas as pd

def calculate_historical_cvar(
        daily_pnl: pd.Series,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> float:
    """Calculate Conditional Value at Risk (CVaR)."""

    if not 0 < confidence_level < 1:
        raise ValueError("[ERROR]: confidence level should be in a valid range (i.e. 0 < c < 1)!")

    if not isinstance(horizon_days, int) or horizon_days < 1:
        raise ValueError(f"[ERROR]: Horizon days ({horizon_days}) should be a postive integer")

    if len(daily_pnl) < horizon_days:
        raise ValueError(f"[ERROR]: Not enough observations to calculate historical VaR! The number of observations ({len(daily_pnl)}) should be larger than the value of horizon days ({horizon_days})!")

    horizon_pnl: pd.Series = pd.Series(
        daily_pnl
        .rolling(window=horizon_days)
        .sum()
        .dropna()
    )

    if horizon_pnl.empty:
        raise ValueError("[ERROR]: Not enough historical PnL data to calculate CVaR!")

    var_threshold: float = horizon_pnl.quantile(
        1 - confidence_level
    )

    tail_losses: pd.Series = horizon_pnl[horizon_pnl <= var_threshold]

    if tail_losses.empty:
        raise ValueError("[ERROR]: No valid observations for CVaR!")

    cvar: float = -float(tail_losses.mean())

    return max(cvar, 0.0)