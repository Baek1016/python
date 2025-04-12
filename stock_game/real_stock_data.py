# real_stock_data.py
import yfinance as yf
from stock_data_source import StockDataSource

class RealStockData(StockDataSource):
    def get_stock_data(self, ticker, period="1mo", interval="1d"):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        return hist
