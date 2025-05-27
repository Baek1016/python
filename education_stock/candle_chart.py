import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle
from data_loader import volumes_by_ticker, dates_by_ticker

def draw_candle_chart(ticker, prices_by_ticker, time_index, output_path="candles", start_display_date=None):
    open_key = f"{ticker}_Open"
    high_key = f"{ticker}_High"
    low_key = f"{ticker}_Low"
    close_key = f"{ticker}_Close"

    # ✅ 무조건 Series로 변환
    open_list = pd.Series(prices_by_ticker[open_key][:time_index+1])
    high_list = pd.Series(prices_by_ticker[high_key][:time_index+1])
    low_list = pd.Series(prices_by_ticker[low_key][:time_index+1])
    close_list = pd.Series(prices_by_ticker[close_key][:time_index+1])
    volume_list = pd.Series(volumes_by_ticker[ticker][:time_index+1])
    date_list = pd.Series(pd.to_datetime(dates_by_ticker[ticker][:time_index+1]))

    # ✅ 날짜 필터링 적용
    if start_display_date:
        start_display_date = pd.to_datetime(start_display_date)
        mask = date_list >= start_display_date
        if mask.sum() == 0:
            print(f"⚠ {ticker}의 최근 1년 데이터가 없음 → 전체 표시")
        else:
            date_list = date_list[mask]
            open_list = open_list[mask]
            high_list = high_list[mask]
            low_list = low_list[mask]
            close_list = close_list[mask]
            volume_list = volume_list[mask]

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    path = os.path.join(output_path, f"{ticker}_candle.png")

    fig = plt.figure(figsize=(10, 6))
    gs = GridSpec(2, 1, height_ratios=[3, 1])
    ax_price = fig.add_subplot(gs[0])
    ax_volume = fig.add_subplot(gs[1], sharex=ax_price)

    if len(date_list) == 0:
        ax_price.set_title("No data available")
    else:
        for i in range(len(date_list)):
            color = 'red' if close_list.iloc[i] >= open_list.iloc[i] else 'green'
            ax_price.plot([date_list.iloc[i], date_list.iloc[i]], [low_list.iloc[i], high_list.iloc[i]], color=color)
            rect = Rectangle(
                (date_list.iloc[i], min(open_list.iloc[i], close_list.iloc[i])),
                width=pd.Timedelta(days=0.8),
                height=abs(open_list.iloc[i] - close_list.iloc[i]),
                color=color
            )
            ax_price.add_patch(rect)

        ax_price.set_ylabel("Price")
        ax_price.grid(True)

        volume_colors = ['red' if close_list.iloc[i] >= open_list.iloc[i] else 'green' for i in range(len(date_list))]
        ax_volume.bar(date_list, volume_list, color=volume_colors, width=0.8)
        ax_volume.set_ylabel("Volume")
        ax_volume.grid(True)
        plt.setp(ax_volume.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    return path
