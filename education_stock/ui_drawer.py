import time
import pygame
import datetime
import os
from constants import LAYOUT, TICKERS
from font_loader import font
from data_loader import prices_by_ticker, volumes_by_ticker, dates_by_ticker, ipo_dates_by_ticker
import game_state
from utils import draw_text
from candle_chart import draw_candle_chart
from events import get_events_for_date, get_persistent_events

def is_stock_listed(ticker, current_date):
    ipo_date = ipo_dates_by_ticker.get(ticker)
    return ipo_date is not None and current_date >= ipo_date

def draw_ui(screen):
    screen.fill((0, 0, 0))
    current_date = game_state.simulation_date_list[game_state.current_day_index]
    if is_stock_listed(game_state.current_ticker, current_date):
        draw_candle_image(screen, game_state.current_ticker, game_state.time_indices[game_state.current_ticker])
    draw_buttons(screen)
    draw_stock_list(screen)
    draw_portfolio(screen)
    draw_total_profit(game_state.time_indices)
    draw_alerts(game_state.alerts)
    draw_news_history(screen, current_date)
    draw_longterm_news(screen, current_date)

def draw_stock_list(screen):
    y = LAYOUT["stock_list"]["y_start"]
    current_date = game_state.simulation_date_list[game_state.current_day_index]
    game_state.visible_tickers.clear()

    for ticker in TICKERS:
        if not is_stock_listed(ticker, current_date):
            continue
        pygame.draw.rect(screen, (0, 0, 255) if ticker == game_state.current_ticker else (230, 230, 230),
                         (LAYOUT["stock_list"]["x"], y, 150, 35))
        draw_text(ticker, LAYOUT["stock_list"]["x"] + 10, y + 8, (255, 255, 255) if ticker == game_state.current_ticker else (0, 0, 0))
        game_state.visible_tickers.append(ticker)
        y += 40

def draw_buttons(screen):
    for label, offset_x in [("Buy", LAYOUT["buttons"]["buy"]["offset_x"]),
                            ("Sell", LAYOUT["buttons"]["sell"]["offset_x"])]:
        x = LAYOUT["screen"]["width"] + offset_x
        y = LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - LAYOUT["buttons"]["buy"]["height"]
        w = LAYOUT["buttons"]["buy"]["width"]
        h = LAYOUT["buttons"]["buy"]["height"]
        pygame.draw.rect(screen, (100, 200, 100) if label == "Buy" else (200, 100, 100), (x, y, w, h))
        draw_text(label, x + 10, y + 10, (255, 255, 255))

def draw_portfolio(screen):
    y = LAYOUT["portfolio"]["y_start"]
    x = LAYOUT["screen"]["width"] + LAYOUT["portfolio"]["x"]
    draw_text("Portfolio", x, y - 30)
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    for ticker, data in game_state.portfolio["stocks"].items():
        if not is_stock_listed(ticker, current_date):
            continue
        qty = data["quantity"]
        if qty > 0 and f"{ticker}_Close" in prices_by_ticker:
            try:
                price = data["buy_price"]
                draw_text(f"{ticker}: {qty} @ ${price:.2f}", x, y, (0, 0, 0))
                y += LAYOUT["portfolio"]["line_height"]
            except Exception as e:
                print(f"📛 포트폴리오 표시 오류: {ticker} - {e}")

def draw_total_profit(time_indices):
    total_invested = 0.0
    total_current_value = 0.0
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    for ticker, data in game_state.portfolio["stocks"].items():
        if not is_stock_listed(ticker, current_date):
            continue
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

def draw_alerts(alerts):
    now = time.time()
    duration = 1.5
    alerts[:] = [entry for entry in alerts if now - entry[1] <= duration]
    for i, (msg, _) in enumerate(alerts[-3:]):
        x = LAYOUT["alerts"]["x"]
        y_base = LAYOUT["alerts"]["y_base"]
        line_height = LAYOUT["alerts"]["line_height"]
        draw_text(msg, x, y_base + i * line_height, (255, 255, 0))

def draw_candle_image(screen, ticker, index):
    path = draw_candle_chart(ticker, prices_by_ticker, index)
    if not os.path.exists(path):
        return
    try:
        image = pygame.image.load(path)
        resized = pygame.transform.smoothscale(image, (900, 600))
        screen.blit(resized, (300, 50))
    except Exception as e:
        print("캔들 이미지 불러오기 실패:", e)

def draw_news_history(screen, current_date):
    x = LAYOUT["news"]["x"]
    y = LAYOUT["news"]["y"]
    width = LAYOUT["news"]["width"]
    max_lines = LAYOUT["news"]["max_lines"]

    pygame.draw.rect(screen, (20, 20, 20), (x, y, width, max_lines * 20 + 10))
    draw_text("📰 News", x + 5, y + 5, (255, 255, 0))

    visible_news = get_events_for_date(current_date)[-max_lines:]
    for i, item in enumerate(visible_news):
        draw_text(item["message"], x + 5, y + 30 + i * 18, (255, 255, 255))

def draw_longterm_news(screen, current_date):
    persistent = get_persistent_events(current_date)
    x, y = LAYOUT["longterm_news"]["x"], LAYOUT["longterm_news"]["y"]
    for line in persistent:
        draw_text(screen, line, x, y, font, (255, 255, 0))
        y += 20