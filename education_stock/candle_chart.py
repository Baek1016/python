# 📁 candle_chart.py

import pandas as pd
import mplfinance as mpf
import os
from data_loader import volumes_by_ticker, dates_by_ticker

def draw_candle_chart(ticker, prices_by_ticker, time_index, output_path="candles"):
    """ 특정 ticker의 OHLCV 데이터를 기반으로 캔들차트를 저장합니다. """
    open_key = f"{ticker}_Open"
    high_key = f"{ticker}_High"
    low_key = f"{ticker}_Low"
    close_key = f"{ticker}_Close"

    # 필요한 데이터 추출
    open_list = prices_by_ticker[open_key][:time_index+1]
    high_list = prices_by_ticker[high_key][:time_index+1]
    low_list = prices_by_ticker[low_key][:time_index+1]
    close_list = prices_by_ticker[close_key][:time_index+1]
    volume_list = volumes_by_ticker[ticker][:time_index+1]
    date_list = dates_by_ticker[ticker][:time_index+1]

    # 날짜를 datetime으로 변환
    df = pd.DataFrame({
        "Open": open_list,
        "High": high_list,
        "Low": low_list,
        "Close": close_list,
        "Volume": volume_list
    }, index=pd.to_datetime(date_list))

    # 저장 폴더 생성
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    path = os.path.join(output_path, f"{ticker}_candle.png")

    # 캔들 차트 저장
    mpf.plot(df, type="candle", volume=True, style="charles", savefig=path)
    return path
