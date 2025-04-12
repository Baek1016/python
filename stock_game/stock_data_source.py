# stock_data_source.py
from abc import ABC, abstractmethod

class StockDataSource(ABC):
    @abstractmethod
    def get_stock_data(self, ticker: str, period: str = "1mo", interval: str = "1d"):
        pass
