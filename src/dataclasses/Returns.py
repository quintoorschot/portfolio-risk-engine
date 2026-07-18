from dataclasses import dataclass, field
import pandas as pd
import numpy as np

@dataclass
class Returns:

    historical_prices: pd.DataFrame = field(repr=False)
    log_returns: list[float] = field(init=False)

    def __post_init__(self) -> None:
        prices: pd.Series = self.historical_prices['market_price']
        self.log_returns = [
            np.log(current / previous)
            for previous, current in zip(prices[:], prices[1:])
        ]

    def __len__(self):
        return len(self.log_returns)
    
    def __getitem__(self, index: int):
        return self.log_returns[index]

    def sort_returns(self) -> None:
        self.log_returns.sort()