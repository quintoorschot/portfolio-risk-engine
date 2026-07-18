from src.dataclasses.Returns import Returns
import numpy as np

def calculate_historical_var(position_value: float, returns: Returns, confidence_interval: float = 0.95) -> float:

    if position_value < 0:
        raise ValueError(f"[ERROR]: Position value ({position_value}) must be non-negative!")
    
    if not 0 < confidence_interval < 1:
        raise ValueError(f"[ERROR]: Confidence interval must be between 0 and 1!")

    n: int = len(returns)

    index = int(np.ceil(n * (1-confidence_interval)) - 1)

    returns.sort_returns()

    value_at_Risk: float = position_value * (1 - np.exp(returns[index]))

    return value_at_Risk