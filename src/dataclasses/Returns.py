from dataclasses import dataclass, field
import numpy as np

@dataclass
class Returns:

    values: list[float]
    log_returns: list[float] = field(init=False)

    def __post_init__(self) -> None:
        self.log_returns = [
            np.log(current / previous)
            for previous, current in zip(self.values[:], self.values[1:])
        ]