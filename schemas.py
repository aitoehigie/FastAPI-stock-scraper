from pydantic import BaseModel

class StockRequest(BaseModel):
    symbol: str


