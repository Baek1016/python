# fake_stock_data.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from stock_data_source import StockDataSource

class FakeStockData(StockDataSource):
    def get_stock_data(self, ticker, period="1mo", interval="1d"):
        days = 30 if period == "1mo" else 7
        interval_minutes = {"1d": 1440, "1h": 60, "15m": 15}.get(interval, 1440)
        points = days * (1440 // interval_minutes)

        dates = [datetime.now() - timedelta(minutes=interval_minutes * i) for i in range(points)]
        dates.reverse()

        prices = np.cumsum(np.random.randn(points)) + 100  # 100부터 시작하는 랜덤워킹
        df = pd.DataFrame(data={"Close": prices}, index=dates)
        return df
