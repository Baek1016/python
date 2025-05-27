import os
import time
import datetime
import pandas as pd
import yfinance as yf
from constants import TICKERS

# 전역 변수
prices_by_ticker = {}
volumes_by_ticker = {}
dates_by_ticker = {}
ipo_dates_by_ticker = {}  # 📌 상장일 저장

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
            "KRW": 1300, "JPY": 150, "EUR": 0.9, "GBP": 0.78, "INR": 83.0
        }

def get_stock_data(ticker, start_date, end_date, retries=3):
    cache_file = os.path.join(CACHE_DIR, f"{ticker}.csv")
    required_cols = ["open", "high", "low", "close", "volume"]

    # 🔄 캐시가 있다면 불러오기
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            df.index = pd.to_datetime(df.index)
            if hasattr(df.index, "tz") and df.index.tz is not None:
                df.index = df.index.tz_convert("UTC").tz_localize(None)

            if df.empty or not all(col in df.columns for col in required_cols):
                raise ValueError("Invalid cache file")
            print(f"📁 캐시 사용: {ticker}")
            return df
        except Exception as e:
            print(f"⚠ 캐시 파일 오류: {ticker} → {e}")
            os.remove(cache_file)

    # 📡 다운로드
    for attempt in range(1, retries + 1):
        try:
            print(f"📡 다운로드 중: {ticker} (시도 {attempt})")
            df = yf.Ticker(ticker).history(start=start_date, end=end_date)
            df.columns = [c.lower() for c in df.columns]
            df = df[required_cols].dropna().astype({"volume": int})

            if df.empty:
                print(f"⚠ {ticker} 데이터 없음")
                return pd.DataFrame()

            df.to_csv(cache_file)
            return df
        except Exception as e:
            print(f"❌ {ticker} 다운로드 실패 (시도 {attempt}): {e}")
            time.sleep(1)

    return pd.DataFrame()

def download_all_stock_data(tickers, start_date="2000-01-01", end_date=None):
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%Y-%m-%d")

    all_dates_set = set()

    for ticker in tickers:
        df = get_stock_data(ticker, start_date, end_date)
        if df.empty:
            print(f"⚠ {ticker} 데이터 없음 → 건너뜀")
            continue

        df.index = pd.to_datetime(df.index)
        if df.index.tz is not None:
            df.index = df.index.tz_convert("UTC").tz_localize(None)

        date_list = df.index.date.tolist()

        prices_by_ticker[f"{ticker}_Open"] = df["open"].tolist()
        prices_by_ticker[f"{ticker}_High"] = df["high"].tolist()
        prices_by_ticker[f"{ticker}_Low"] = df["low"].tolist()
        prices_by_ticker[f"{ticker}_Close"] = df["close"].tolist()
        volumes_by_ticker[ticker] = df["volume"].tolist()
        dates_by_ticker[ticker] = date_list

        ipo_dates_by_ticker[ticker] = date_list[0] if date_list else None
        all_dates_set.update(date_list)

    simulation_dates = sorted(all_dates_set)
    print("✅ 데이터 다운로드 완료")
    print(f"📊 시뮬레이션 날짜 수: {len(simulation_dates)}")
    return simulation_dates

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
    "ipo_dates_by_ticker"
]
