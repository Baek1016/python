# main.py
from real_stock_data import RealStockData
from fake_stock_data import FakeStockData

# 실제 데이터 사용할지, 가짜 데이터 사용할지 선택
use_real_data = False  # True로 바꾸면 yfinance로 실제 주식 가져옴

# 데이터 소스 선택
data_source = RealStockData() if use_real_data else FakeStockData()

# 예시: 주식 데이터 가져오기
stock_data = data_source.get_stock_data("AAPL", period="1mo", interval="1d")

# 여기서부터 pygame으로 그래프 그리기, 시뮬레이션 로직 사용하면 됨
print(stock_data.tail())  # 확인용 출력
