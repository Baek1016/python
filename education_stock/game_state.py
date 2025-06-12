#game_state.py
import datetime
import time
import pygame
import sys
from constants import TICKERS, LAYOUT
import os


from data_loader import (
    download_all_stock_data,
    prices_by_ticker,
    dates_by_ticker,
    ipo_dates_by_ticker,
    calculate_current_prices_usd  # ✅ 환율 기반 현재가 추가
)
from profit_tracker import calculate_total_profit, plot_profit_history
from events import schedule_random_events, get_events_for_date
from portfolio_manager import buy_stock, sell_stock

# 전역 상태 정의
game_mode = "menu"
simulation_date_list = []
current_day_index = 0
current_ticker = None
time_indices = {}
portfolio = {}
alerts = []
visible_tickers = [] 
news_log = []

screen = pygame.display.set_mode((2000, 1280))
comparison_tickers = []
comparison_mode = False
show_comparison_charts = False
zoom_comparison_mode = False

input_mode = None
input_text = ""
load_file_buttons = []

profit_history = []

game_mode = "menu"  # 시작 시 메뉴 모드 (menu, play, load)

selected_save_file = None
load_file_buttons = []
input_mode = None
input_text = ""


# ✅ 선택 색상 정의
selection_colors = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (128, 0, 128)]

zoom_scroll_offset = 0
zoom_level_index = 0
dragging = False
last_mouse_pos = (0, 0)

zoom_levels = [0.5, 0.8, 1.0, 1.5, 2.0]
zoom_level_index = 2  # 기본은 1.0배
grid_button_rects = {} 
top10_button_rects = {}  # 좌측 순위 버튼 rect → ticker 매핑용

def init_game():
    global simulation_date_list, current_ticker, time_indices, portfolio, game_mode

    print("📱 데이터 다운로드 시작...")
    simulation_date_list = download_all_stock_data(list(TICKERS.keys()))

    if not simulation_date_list:
        print("❌ 날짜 리스트 없음 → 게임 시작 불가")
        sys.exit()

    print(f"✅ 총 시뮬리언 날짜 수: {len(simulation_date_list)}")
    print(f"🗅️ 시작일: {simulation_date_list[0]}")
    print(f"🗅️ 종료일: {simulation_date_list[-1]}")

    portfolio.update({
        "cash": 100000.0,
        "stocks": {ticker: {"quantity": 0, "buy_price": 0.0} for ticker in TICKERS}
    })

    time_indices.update({ticker: 0 for ticker in TICKERS})

    for ticker in TICKERS:
        if is_stock_listed(ticker, simulation_date_list[0]):
            current_ticker = ticker
            break

    schedule_random_events(list(TICKERS.keys()), simulation_date_list)
    calculate_current_prices_usd()  # ✅ 현재가 계산
    game_mode = "playing"

def main_loop(screen):
    global current_day_index, input_mode, input_text, zoom_scroll_offset, zoom_level_index, dragging, last_mouse_pos

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse_pos = event.pos
                handle_mouse_click(event.pos)
                handle_button_click(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx, dy = event.pos[0] - last_mouse_pos[0], event.pos[1] - last_mouse_pos[1]
                    zoom_scroll_offset += dy
                    last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                if zoom_comparison_mode:
                    if event.y > 0 and zoom_level_index < len(zoom_levels) - 1:
                        zoom_level_index += 1
                    elif event.y < 0 and zoom_level_index > 0:
                        zoom_level_index -= 1
            elif event.type == pygame.KEYDOWN:
                if input_mode in ("save", "load"):
                    if event.key == pygame.K_RETURN:
                        input_mode = None
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.key == pygame.K_ESCAPE and zoom_comparison_mode:
                    toggle_zoom_mode()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                LAYOUT["screen"]["width"] = event.w
                LAYOUT["screen"]["height"] = event.h

        if game_mode == "playing":
            current_day_index += 1
            if current_day_index >= len(simulation_date_list):
                print("🗅️ 모든 날짜 종료")
                break

            current_date = simulation_date_list[current_day_index]
            apply_news_events(current_date, current_day_index)

            for ticker in time_indices:
                if time_indices[ticker] < len(simulation_date_list) - 1:
                    time_indices[ticker] += 1

            total_profit = calculate_total_profit()
            profit_history.append(total_profit)
            plot_profit_history(profit_history)

        from ui_drawer import draw_ui
        draw_ui(screen)

        pygame.display.flip()
        clock.tick(5)

def handle_mouse_click(pos):
    x, y = pos
    current_date = simulation_date_list[current_day_index]

    for ticker, rect in grid_button_rects.items():
        if rect.collidepoint(x, y):
            global current_ticker
            if comparison_mode:
                toggle_ticker_selection(ticker)
            else:
                current_ticker = ticker
                alerts.append((f"Selected: {ticker}", time.time()))

    for ticker, rect in top10_button_rects.items():
        if rect.collidepoint(x, y):
            current_ticker = ticker
            alerts.append((f"Selected from Top10: {ticker}", time.time()))
            return

def handle_button_click(pos):
    x, y = pos
    width = LAYOUT["buttons"]["buy"]["width"]
    height = LAYOUT["buttons"]["buy"]["height"]
    buy_x = LAYOUT["screen"]["width"] + LAYOUT["buttons"]["buy"]["offset_x"]
    sell_x = LAYOUT["screen"]["width"] + LAYOUT["buttons"]["sell"]["offset_x"]
    btn_y = LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - height

    buy_rect = pygame.Rect(buy_x, btn_y, width, height)
    sell_rect = pygame.Rect(sell_x, btn_y, width, height)

    if buy_rect.collidepoint(x, y):
        print(f"🟢 Buy 클릭됨: {current_ticker}")
        buy_stock(current_ticker, 1)
    elif sell_rect.collidepoint(x, y):
        print(f"🔴 Sell 클릭됨: {current_ticker}")
        sell_stock(current_ticker, 1)

    compare_btn_rect = pygame.Rect(
        LAYOUT["comparison"]["x"],
        LAYOUT["comparison"]["y"],
        LAYOUT["comparison"]["width"],
        LAYOUT["comparison"]["height"]
    )
    if compare_btn_rect.collidepoint(x, y):
        global comparison_mode, show_comparison_charts
        toggle_comparison_mode()
        show_comparison_charts = comparison_mode
        print(f"📊 비교 모드 전환: {comparison_mode}")

    clear_btn_rect = pygame.Rect(230, 20, 160, 30)
    if clear_btn_rect.collidepoint(x, y) and comparison_mode:
        comparison_tickers.clear()
        print("🪹 선택 초기화")

    zoom_btn_rect = pygame.Rect(
        LAYOUT["zoom"]["x"], LAYOUT["zoom"]["y"],
        LAYOUT["zoom"]["width"], LAYOUT["zoom"]["height"]
    )
    if zoom_btn_rect.collidepoint(x, y) and comparison_mode and comparison_tickers:
        toggle_zoom_mode()

def toggle_zoom_mode():
    global zoom_comparison_mode
    zoom_comparison_mode = not zoom_comparison_mode

def apply_news_events(current_date, current_index):
    events = get_events_for_date(current_date)
    for event in events:
        key = f"{event['ticker']}_Close"
        if key in prices_by_ticker and current_index < len(prices_by_ticker[key]):
            prices_by_ticker[key][current_index] *= (1 + event["impact"])
            alerts.append((event["message"], time.time()))
            news_log.append({"date": current_date, "message": event["message"]})
            print(f"📢 뉴스 적용: {event['ticker']} - {event['message']}")

def is_stock_listed(ticker, current_date):
    ipo_date = ipo_dates_by_ticker.get(ticker)
    return ipo_date is not None and current_date >= ipo_date

def toggle_comparison_mode():
    global comparison_mode, comparison_tickers
    comparison_mode = not comparison_mode
    if not comparison_mode:
        comparison_tickers.clear()

def toggle_ticker_selection(ticker):
    global comparison_tickers
    if ticker in comparison_tickers:
        comparison_tickers.remove(ticker)
    else:
        if len(comparison_tickers) < 4:
            comparison_tickers.append(ticker)
