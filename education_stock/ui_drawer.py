# ui_drawer.py (최신 전체 통합 버전)

import time
import pygame
import datetime
from constants import LAYOUT, TICKERS
from font_loader import font
from data_loader import prices_by_ticker, volumes_by_ticker, dates_by_ticker
import game_state
from utils import draw_text
from candle_chart import draw_candle_chart
import os

# ✅ draw_ui: 메인 UI 구성

def draw_ui(screen):
    screen.fill((0, 0, 0))
    draw_chart(screen)
    draw_buttons(screen)
    draw_stock_list(screen)
    draw_portfolio(screen)
    draw_total_profit(game_state.time_indices)
    draw_alerts(game_state.alerts)
    draw_candle_image(screen, game_state.current_ticker, game_state.time_indices[game_state.current_ticker])


# ✅ draw_chart: 종가 기준 선형 차트

def draw_chart(screen):
    if not game_state.current_ticker:
        return

    ticker = game_state.current_ticker
    key = f"{ticker}_Close"
    if key not in prices_by_ticker:
        return

    prices = prices_by_ticker[key]
    index = game_state.time_indices.get(ticker, 0)

    if index < 1 or len(prices) < 2:
        return

    chart_rect = pygame.Rect(
        LAYOUT["chart"]["x"],
        LAYOUT["chart"]["y"],
        LAYOUT["chart"]["width"],
        LAYOUT["chart"]["height"]
    )
    pygame.draw.rect(screen, (220, 220, 220), chart_rect)

    max_price = max(prices[:index + 1])
    min_price = min(prices[:index + 1])
    if max_price == min_price:
        max_price += 1

    chart_w = chart_rect.width
    chart_h = chart_rect.height
    offset_x = chart_rect.x
    offset_y = chart_rect.y

    points = []
    for i in range(index + 1):
        x = offset_x + (i / max(index, 1)) * chart_w
        price = prices[i]
        y = offset_y + chart_h - ((price - min_price) / (max_price - min_price)) * chart_h
        points.append((x, y))

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 100, 255), False, points, 2)

    # 거래량 표시
    volumes = volumes_by_ticker.get(ticker, [])
    if volumes and index >= 1:
        max_vol = max(volumes[:index + 1])
        for i in range(index + 1):
            x = offset_x + (i / max(index, 1)) * chart_w
            vol_height = (volumes[i] / max_vol) * (chart_h * 0.25)  # 하단 25%
            y = offset_y + chart_h - vol_height
            pygame.draw.rect(screen, (150, 150, 150), (x, y, 2, vol_height))


def draw_volume_bars(screen, ticker, index, chart_rect):
    volumes = volumes_by_ticker.get(ticker, [])
    if not volumes or index < 1:
        return

    sub_volumes = volumes[:index + 1]
    max_volume = max(sub_volumes)
    if max_volume == 0:
        return

    bar_area_height = 60  # 차트 아래 공간 높이
    bar_top = chart_rect.bottom + 5
    bar_width = chart_rect.width / len(sub_volumes)

    for i, v in enumerate(sub_volumes):
        x = chart_rect.x + i * bar_width
        h = (v / max_volume) * bar_area_height
        y = bar_top + (bar_area_height - h)
        pygame.draw.rect(screen, (150, 150, 150), (x, y, bar_width * 0.8, h))



# ✅ draw_buttons: Buy / Sell 버튼

def draw_buttons(screen):
    for label, offset_x in [("Buy", LAYOUT["buttons"]["buy"]["offset_x"]),
                            ("Sell", LAYOUT["buttons"]["sell"]["offset_x"])]:
        x = LAYOUT["screen"]["width"] + offset_x
        y = LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - LAYOUT["buttons"]["buy"]["height"]
        w = LAYOUT["buttons"]["buy"]["width"]
        h = LAYOUT["buttons"]["buy"]["height"]
        pygame.draw.rect(screen, (100, 200, 100) if label == "Buy" else (200, 100, 100), (x, y, w, h))
        draw_text(label, x + 10, y + 10, (255, 255, 255))


# ✅ draw_stock_list: 종목 리스트

def draw_stock_list(screen):
    y = LAYOUT["stock_list"]["y_start"]
    for i, ticker in enumerate(list(TICKERS.keys())[:10]):
        pygame.draw.rect(screen, (230, 230, 230), (LAYOUT["stock_list"]["x"], y + i * 40, 150, 35))
        draw_text(ticker, LAYOUT["stock_list"]["x"] + 10, y + i * 40 + 8, (0, 0, 0))


# ✅ draw_portfolio: 보유 주식 목록

def draw_portfolio(screen):
    y = LAYOUT["portfolio"]["y_start"]
    x = LAYOUT["screen"]["width"] + LAYOUT["portfolio"]["x"]
    draw_text("Portfolio", x, y - 30)

    for ticker, data in game_state.portfolio["stocks"].items():
        qty = data["quantity"]
        price = data["buy_price"]
        if qty > 0:
            draw_text(f"{ticker}: {qty} @ ${price:.2f}", x, y, (0, 0, 0))
            y += LAYOUT["portfolio"]["line_height"]


# ✅ draw_total_profit: 전체 수익률

def draw_total_profit(time_indices):
    total_invested = 0.0
    total_current_value = 0.0
    for ticker, data in game_state.portfolio["stocks"].items():
        quantity = data["quantity"]
        if quantity > 0:
            invested = quantity * data["buy_price"]
            current_price = float(prices_by_ticker[f"{ticker}_Close"][time_indices[ticker]])
            current_value = quantity * current_price
            total_invested += invested
            total_current_value += current_value

    if total_invested > 0:
        total_profit = total_current_value - total_invested
        profit_percent = (total_profit / total_invested) * 100
    else:
        total_profit = 0
        profit_percent = 0

    color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)
    x = LAYOUT["profit_summary"]["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x
    y = LAYOUT["profit_summary"]["y"]

    draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y, color)


# ✅ draw_alerts: 알림 메시지 출력

def draw_alerts(alerts):
    now = time.time()
    duration = 1.5
    alerts[:] = [entry for entry in alerts if now - entry[1] <= duration]
    for i, (msg, _) in enumerate(alerts[-3:]):
        x = LAYOUT["alerts"]["x"]
        y_base = LAYOUT["alerts"]["y_base"]
        line_height = LAYOUT["alerts"]["line_height"]
        draw_text(msg, x, y_base + i * line_height, (255, 255, 0))


# ui_drawer.py의 draw_portfolio()에서 아래처럼 출력 개선:
def draw_portfolio(screen):
    y = LAYOUT["portfolio"]["y_start"]
    x = LAYOUT["screen"]["width"] + LAYOUT["portfolio"]["x"]
    draw_text("Portfolio", x, y - 30)

    for ticker, data in game_state.portfolio["stocks"].items():
        qty = data["quantity"]
        price = data["buy_price"]
        if qty > 0:
            draw_text(f"{ticker}: {qty} @ ${price:.2f}", x, y, (0, 0, 0))
            y += LAYOUT["portfolio"]["line_height"]

# ✨ 실제 캔들차트 이미지 로드 및 화면 출력
def draw_candle_image(screen, ticker, index):
    path = draw_candle_chart(ticker, prices_by_ticker, index)
    if os.path.exists(path):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (300, 200))  # 크기 조절
        screen.blit(image, (800, 500))  # 위치 조절
