import os
import time
import datetime
import pandas as pd
import yfinance as yf
from constants import TICKERS
from concurrent.futures import ThreadPoolExecutor

# 전역 변수들
prices_by_ticker = {}
volumes_by_ticker = {}
dates_by_ticker = {}
simulation_date_list = []  # ✅ 모든 종목에서 공통된 날짜 리스트

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def get_exchange_rates(base="USD"):
    import requests
    try:
        url = f"https://api.exchangerate.host/latest?base={base}"
        response = requests.get(url, timeout=3)
        data = response.json()
        if "rates" not in data:
            raise ValueError("Missing 'rates' in API response")
        return data["rates"]
    except Exception as e:
        print("⚠ 환율 정보 가져오기 실패:", e)
        return {
            "KRW": 1300,
            "JPY": 150,
            "EUR": 0.9,
            "GBP": 0.78,
            "INR": 83.0
        }

def get_stock_data(ticker, start_date, end_date):
    cache_file = os.path.join(CACHE_DIR, f"{ticker}.csv")
    required_cols = ["open", "high", "low", "close", "volume"]

    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file, index_col=0, encoding="utf-8-sig")
            if df.empty or not all(col in df.columns for col in required_cols):
                raise ValueError("Missing required columns")
            return df
        except Exception as e:
            print(f"⚠ 캐시 파일 오류: {ticker} → {e}")
            os.remove(cache_file)

    try:
        print(f"📡 다운로드 중: {ticker}")
        time.sleep(1)
        df = yf.Ticker(ticker).history(start=start_date, end=end_date, interval="1d", auto_adjust=False)
        df.columns = [col.lower() for col in df.columns]
        df = df[required_cols].dropna().astype({"volume": int})
        df.to_csv(cache_file, encoding="utf-8-sig")
        return df
    except Exception as e:
        print(f"❌ {ticker} 데이터 다운로드 실패: {e}")
        return pd.DataFrame()

def download_all_stock_data(start_date="2000-01-01", end_date=None):
    global simulation_date_list

    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    all_dates_set = set()

    def download_one(ticker):
        df = get_stock_data(ticker, start_date, end_date)
        if df.empty:
            return

        prices_by_ticker[f"{ticker}_Open"] = df["open"].tolist()
        prices_by_ticker[f"{ticker}_High"] = df["high"].tolist()
        prices_by_ticker[f"{ticker}_Low"] = df["low"].tolist()
        prices_by_ticker[f"{ticker}_Close"] = df["close"].tolist()
        volumes_by_ticker[ticker] = df["volume"].tolist()

        date_list = [pd.to_datetime(idx).date() for idx in df.index]
        dates_by_ticker[ticker] = date_list
        all_dates_set.update(date_list)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(download_one, TICKERS)

    simulation_date_list = sorted(all_dates_set)

    print("✅ 데이터 다운로드 완료")
    print(f"총 티커 수: {len(prices_by_ticker) // 4}")
    print(f"총 시뮬레이션 날짜 수: {len(simulation_date_list)}")

def clear_cache():
    deleted = 0
    for fname in os.listdir(CACHE_DIR):
        if fname.endswith(".csv"):
            os.remove(os.path.join(CACHE_DIR, fname))
            deleted += 1
    print(f"🗑️ 캐시 {deleted}개 삭제됨")

__all__ = [
    "get_exchange_rates",
    "get_stock_data",
    "download_all_stock_data",
    "clear_cache",
    "prices_by_ticker",
    "volumes_by_ticker",
    "dates_by_ticker",
    "simulation_date_list"
]
