import time
import pygame
import os
from constants import LAYOUT, TICKERS
from font_loader import font
from data_loader import prices_by_ticker, volumes_by_ticker, dates_by_ticker, ipo_dates_by_ticker
import game_state
from utils import draw_text
from candle_chart import draw_candle_chart
from events import get_events_for_date, get_persistent_events

selection_colors = [
    (0, 102, 255),   # 파랑
    (0, 204, 102),   # 초록
    (255, 102, 102), # 빨강
    (153, 102, 255), # 보라
]

def is_stock_listed(ticker, current_date):
    ipo_date = ipo_dates_by_ticker.get(ticker)
    return ipo_date is not None and current_date >= ipo_date

def draw_ui(screen):
    screen.fill((0, 0, 0))
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    if game_state.zoom_comparison_mode:
        draw_comparison_charts_zoomed(screen)
    elif game_state.comparison_mode and game_state.comparison_tickers:
        draw_comparison_charts_candlestick(screen)
    else:
        if is_stock_listed(game_state.current_ticker, current_date):
            draw_candle_image(screen, game_state.current_ticker, game_state.time_indices[game_state.current_ticker])

    draw_buttons(screen)
    draw_stock_list(screen)
    draw_portfolio(screen)
    draw_total_profit(screen, game_state.time_indices)
    draw_alerts(screen, game_state.alerts)
    draw_news_history(screen, current_date)
    draw_longterm_news(screen, current_date)
    draw_comparison_button(screen)
    draw_selected_tickers(screen)
    draw_clear_button(screen)
    draw_zoom_button(screen)
    draw_all_companies_grid(screen)
    draw_top_10_by_profit(screen)
    draw_all_companies_grid(screen)

def draw_buttons(screen):
    for label, offset_x in [("Buy", LAYOUT["buttons"]["buy"]["offset_x"]),
                            ("Sell", LAYOUT["buttons"]["sell"]["offset_x"])]:
        x = LAYOUT["screen"]["width"] + offset_x
        y = LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - LAYOUT["buttons"]["buy"]["height"]
        w = LAYOUT["buttons"]["buy"]["width"]
        h = LAYOUT["buttons"]["buy"]["height"]
        color = (100, 200, 100) if label == "Buy" else (200, 100, 100)
        pygame.draw.rect(screen, color, (x, y, w, h))
        draw_text(label, x + 10, y + 5, (0, 0, 0), screen)

def draw_comparison_button(screen):
    rect = pygame.Rect(LAYOUT["comparison"]["x"], LAYOUT["comparison"]["y"],
                       LAYOUT["comparison"]["width"], LAYOUT["comparison"]["height"])
    color = (255, 255, 0) if not game_state.comparison_mode else (100, 100, 100)
    pygame.draw.rect(screen, color, rect)
    draw_text("Select Mode" if not game_state.comparison_mode else "Exit Select", rect.x + 10, rect.y + 10, (0, 0, 0), screen)

def draw_clear_button(screen):
    if not game_state.comparison_mode:
        return
    rect = pygame.Rect(240, 10, 140, 40)
    pygame.draw.rect(screen, (200, 80, 80), rect)
    draw_text("Clear Selection", rect.x + 10, rect.y + 10, (0, 0, 0), screen)

def draw_zoom_button(screen):
    if not game_state.comparison_mode or not game_state.comparison_tickers:
        return
    rect = pygame.Rect(LAYOUT["zoom"]["x"], LAYOUT["zoom"]["y"], LAYOUT["zoom"]["width"], LAYOUT["zoom"]["height"])
    pygame.draw.rect(screen, (80, 160, 240), rect)
    draw_text("\U0001f50d Zoom Mode", rect.x + 10, rect.y + 10, (0, 0, 0), screen)

def draw_selected_tickers(screen):
    if not game_state.comparison_mode:
        return
    x = 400
    y = 10
    for i, ticker in enumerate(game_state.comparison_tickers):
        color = selection_colors[i % len(selection_colors)]
        draw_text(f"{i+1}. {ticker}", x, y + i * 22, color, screen)

def draw_stock_list(screen):
    y = LAYOUT["stock_list"]["y_start"]
    current_date = game_state.simulation_date_list[game_state.current_day_index]
    game_state.visible_tickers.clear()

    for ticker in TICKERS:
        if not is_stock_listed(ticker, current_date):
            continue
        if ticker in game_state.comparison_tickers:
            idx = game_state.comparison_tickers.index(ticker)
            rect_color = selection_colors[idx % len(selection_colors)]
        elif ticker == game_state.current_ticker:
            rect_color = (0, 0, 255)
        else:
            rect_color = (230, 230, 230)
        pygame.draw.rect(screen, rect_color, (LAYOUT["stock_list"]["x"], y, 150, 35))
        text_color = (255, 255, 255) if rect_color != (230, 230, 230) else (0, 0, 0)
        draw_text(ticker, LAYOUT["stock_list"]["x"] + 10, y + 8, text_color, screen)
        game_state.visible_tickers.append(ticker)
        y += 40

def draw_portfolio(screen):
    y = LAYOUT["portfolio"]["y_start"]
    x = LAYOUT["portfolio"]["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x
    draw_text("Portfolio", x, y - 30, (255, 255, 255), screen)
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    for ticker, data in game_state.portfolio["stocks"].items():
        if not is_stock_listed(ticker, current_date):
            continue
        qty = data["quantity"]
        if qty > 0 and f"{ticker}_Close" in prices_by_ticker:
            try:
                price = data["buy_price"]
                draw_text(f"{ticker}: {qty} @ ${price:.2f}", x, y, (255, 255, 255), screen)
                y += LAYOUT["portfolio"]["line_height"]
            except Exception as e:
                print(f"\U0001f4cb 포트폴리오 표시 오류: {ticker} - {e}")

def draw_total_profit(screen, time_indices):
    total_invested, total_current_value = 0.0, 0.0
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    for ticker, data in game_state.portfolio["stocks"].items():
        if not is_stock_listed(ticker, current_date):
            continue
        qty = data["quantity"]
        if qty > 0:
            invested = qty * data["buy_price"]
            try:
                current_price = float(prices_by_ticker[f"{ticker}_Close"][time_indices[ticker]])
                current_value = qty * current_price
                total_invested += invested
                total_current_value += current_value
            except Exception as e:
                print(f"⚠️ 수익 계산 오류 ({ticker}): {e}")

    total_profit = total_current_value - total_invested
    profit_percent = (total_profit / total_invested) * 100 if total_invested > 0 else 0
    color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)
    x = LAYOUT["profit_summary"]["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x
    y = LAYOUT["profit_summary"]["y"]
    draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y, color, screen)

def draw_alerts(screen, alerts):
    now = time.time()
    duration = 1.5
    alerts[:] = [entry for entry in alerts if now - entry[1] <= duration]
    for i, (msg, _) in enumerate(alerts[-3:]):
        x = LAYOUT["alerts"]["x"]
        y = LAYOUT["alerts"]["y_base"] + i * LAYOUT["alerts"]["line_height"]
        draw_text(msg, x, y, (255, 255, 0), screen)

def draw_candle_image(screen, ticker, index):
    path = draw_candle_chart(ticker, prices_by_ticker, index)
    if os.path.exists(path):
        try:
            image = pygame.image.load(path)
            resized = pygame.transform.smoothscale(image, (900, 600))
            screen.blit(resized, (300, 50))
        except Exception as e:
            print("⚠️ 캔들 이미지 불러오기 실패:", e)

def draw_news_history(screen, current_date):
    if game_state.zoom_comparison_mode:
        return  # 확대 모드에서는 뉴스 미표시
    x, y = LAYOUT["news"]["x"], LAYOUT["news"]["y"]
    width, max_lines = LAYOUT["news"]["width"], LAYOUT["news"]["max_lines"]
    pygame.draw.rect(screen, (20, 20, 20), (x, y, width, max_lines * 20 + 10))
    draw_text("\U0001f4f0 News", x + 5, y + 5, (255, 255, 0), screen)

    # ✅ 최근 N개 뉴스 출력 (최근 순서로)
    latest_news = game_state.news_log[-max_lines:]
    for i, item in enumerate(latest_news):
        draw_text(item["message"], x + 5, y + 30 + i * 18, (255, 255, 255), screen)


def draw_longterm_news(screen, current_date):
    x, y = LAYOUT["longterm_news"]["x"], LAYOUT["longterm_news"]["y"]
    draw_text("\U0001f4e2 Persistent Rumors", x, y, (255, 200, 0), screen)
    for i, line in enumerate(get_persistent_events(current_date)):
        draw_text(line, x, y + 25 + i * 20, (255, 255, 255), screen)

def draw_comparison_charts_candlestick(screen):
    tickers = game_state.comparison_tickers
    if not tickers:
        return
    width, height, padding = 400, 300, 20
    cols = 2
    start_x, start_y = 250, 100
    for idx, ticker in enumerate(tickers):
        row, col = idx // cols, idx % cols
        x = start_x + col * (width + padding)
        y = start_y + row * (height + padding)
        index = game_state.time_indices[ticker]
        path = draw_candle_chart(ticker, prices_by_ticker, index)
        if os.path.exists(path):
            try:
                image = pygame.image.load(path)
                resized = pygame.transform.smoothscale(image, (width, height))
                screen.blit(resized, (x, y))
                draw_text(ticker, x + 10, y + 10, (255, 255, 255), screen)
            except Exception as e:
                print(f"⚠️ 비교 차트 로딩 오류 ({ticker}): {e}")

def draw_comparison_charts_zoomed(screen):
    tickers = game_state.comparison_tickers
    if not tickers:
        return
    zoom = game_state.zoom_levels[game_state.zoom_level_index]
    start_y = 50 + game_state.zoom_scroll_offset
    chart_height = int(300 * zoom)
    chart_width = int(1000 * zoom)
    padding = 30
    for idx, ticker in enumerate(tickers):
        index = game_state.time_indices[ticker]
        path = draw_candle_chart(ticker, prices_by_ticker, index)
        if os.path.exists(path):
            try:
                image = pygame.image.load(path)
                resized = pygame.transform.smoothscale(image, (chart_width, chart_height))
                screen.blit(resized, (100, start_y))
                draw_text(ticker, 110, start_y + 10, (255, 255, 255), screen)
                start_y += chart_height + padding
            except Exception as e:
                print(f"⚠️ 확대 차트 로딩 실패 ({ticker}): {e}")

import math

def draw_all_companies_grid(screen):

    tickers = game_state.visible_tickers
    if not tickers:
        return

    # 💡 레이아웃 설정
    max_rows = 5
    cell_width = 180
    cell_height = 40
    padding_x = 10
    padding_y = 8

    cols = math.ceil(len(tickers) / max_rows)

    # ✅ 시작 위치: 화면 맨 아래로부터 위로 올라오게
    start_x = 100  # 좌측 여백
    start_y = LAYOUT["screen"]["height"] - (cell_height + padding_y) * max_rows - 20

    game_state.grid_button_rects = {}

    for i, ticker in enumerate(tickers):
        row = i % max_rows
        col = i // max_rows

        x = start_x + col * (cell_width + padding_x)
        y = start_y + row * (cell_height + padding_y)

        # 선택 색상 처리
        if ticker == game_state.current_ticker:
            color = (0, 128, 255)
        elif ticker in game_state.comparison_tickers:
            idx = game_state.comparison_tickers.index(ticker)
            color = selection_colors[idx % len(selection_colors)]
        else:
            color = (230, 230, 230)

        pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
        text_color = (0, 0, 0) if color == (230, 230, 230) else (255, 255, 255)
        rect = pygame.Rect(x, y, cell_width, cell_height)
        game_state.grid_button_rects[ticker] = rect
        pygame.draw.rect(screen, color, rect)
        draw_text(ticker, x + 10, y + 10, text_color, screen)

def draw_top_10_by_profit(screen):
    profit_list = []
    for ticker, data in game_state.portfolio["stocks"].items():
        qty = data["quantity"]
        if f"{ticker}_Close" in prices_by_ticker and game_state.time_indices.get(ticker) is not None:
            try:
                buy_price = data["buy_price"]
                current_price = prices_by_ticker[f"{ticker}_Close"][game_state.time_indices[ticker]]
                if qty > 0 or buy_price > 0:
                    profit = ((current_price - buy_price) / buy_price) if buy_price else 0
                    profit_list.append((ticker, profit))
            except:
                continue

    sorted_list = sorted(profit_list, key=lambda x: x[1], reverse=True)[:10]

    x, y = LAYOUT["stock_list"]["x"], LAYOUT["stock_list"]["y_start"]
    for i, (ticker, profit) in enumerate(sorted_list):
        color = (0, 0, 255) if ticker == game_state.current_ticker else (230, 230, 230)
        pygame.draw.rect(screen, color, (x, y + i * 40, 150, 35))
        text_color = (255, 255, 255) if color != (230, 230, 230) else (0, 0, 0)
        draw_text(f"{ticker}", x + 10, y + i * 40 + 8, text_color, screen)
