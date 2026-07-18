from dataclasses import dataclass, field

@dataclass
class Position:

    portfolio_id: str
    position_id: str
    instrument_id: str
    quantity: float
    market_price: float

    def __post_init__(self) -> None:

        if self.market_price < 0:
            raise ValueError("[ERROR]: Market price must be non-negative!")
        
    @property
    def total_value(self) -> float:
        return self.quantity * self.market_price