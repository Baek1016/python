# game_state.py
import datetime
import time
import pygame
import sys
import os
from constants import TICKERS, LAYOUT
from data_loader import (
    download_all_stock_data,
    prices_by_ticker,
    dates_by_ticker,
    ipo_dates_by_ticker,
    calculate_current_prices_usd
)
from profit_tracker import calculate_total_profit, plot_profit_history
from events import schedule_random_events, get_events_for_date
from portfolio_manager import buy_stock, sell_stock
from save_manager import load_game, delete_game

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
selected_save_file = None
profit_history = []

selection_colors = [(0, 0, 255), (0, 128, 0), (255, 0, 0), (128, 0, 128)]

zoom_scroll_offset = 0
zoom_level_index = 0
dragging = False
last_mouse_pos = (0, 0)

zoom_levels = [0.5, 0.8, 1.0, 1.5, 2.0]
zoom_level_index = 2

grid_button_rects = {}
top10_button_rects = {}

day_duration = 10  # 하루 진행에 10초 사용
day_start_time = None  # 초기엔 None으로 둔다

def init_game():
    global simulation_date_list, current_ticker, time_indices, portfolio, game_mode

    print("📱 데이터 다운로드 시작...")
    simulation_date_list = download_all_stock_data(list(TICKERS.keys()))

    if not simulation_date_list:
        print("❌ 날짜 리스트 없음 → 게임 시작 불가")
        sys.exit()

    print(f"✅ 총 시무리언 날짜 수: {len(simulation_date_list)}")
    print(f"🗕️ 시작일: {simulation_date_list[0]}")
    print(f"🗕️ 종료일: {simulation_date_list[-1]}")

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
    calculate_current_prices_usd(simulation_date_list)
    game_mode = "playing"

def main_loop(screen):
    from ui_drawer import draw_load_file_buttons
    global current_day_index, input_mode, input_text, zoom_scroll_offset, zoom_level_index, dragging, last_mouse_pos
    clock = pygame.time.Clock()
    running = True
    global day_start_time  # 전역 변수 사용 명시
    if day_start_time is None:
        day_start_time = time.time()

    while running:
        screen.fill((0, 0, 0))

        if game_mode == "load_menu":
            draw_load_file_buttons(screen)
            pygame.display.flip()
            clock.tick(5)
            continue

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

                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    input_mode = "save"
                    input_text = ""

        # 반복문 안에서 시간 흐름 제어
        if game_mode == "playing":
            current_date = simulation_date_list[current_day_index]

            # 거래일이 아닌 경우 바로 넘김
            if not any(current_date == d for d in dates_by_ticker.get(current_ticker, [])):
                current_day_index += 1
                day_start_time = time.time()  # 새로운 날 시작
                continue
            
            # 아직 10초가 안 지났으면 대기
            if time.time() - day_start_time < day_duration:
                from ui_drawer import draw_ui
                draw_ui(screen)
                pygame.display.flip()
                clock.tick(30)
                continue  # 하루 대기 중
            
            # 10초가 지난 경우 실제 하루 진행
            current_day_index += 1
            day_start_time = time.time()  # 다음 날 시작

            if current_day_index >= len(simulation_date_list):
                print("🗕️ 모든 날짜 종료")
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
    global selected_save_file, game_mode

    if game_mode == "load_menu":
        for filename, load_btn, del_btn in load_file_buttons:
            if load_btn.collidepoint(pos):
                print(f"📅 로드 시도: {filename}")
                data = load_game(filename)
                load_game_data_into_state(data)
                game_mode = "playing"
            elif del_btn.collidepoint(pos):
                print(f"🗑 삭제 시도: {filename}")
                delete_game(filename)
        return

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
        print("🩹 선택 초기화")

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

def load_game_data_into_state(data):
    global simulation_date_list, current_day_index, current_ticker, time_indices, portfolio, alerts, news_log, profit_history
    simulation_date_list = data["simulation_date_list"]
    current_day_index = data["current_day_index"]
    current_ticker = data["current_ticker"]
    time_indices = data["time_indices"]
    portfolio = data["portfolio"]
    alerts = []
    news_log = data.get("news_log", [])
    profit_history = data.get("profit_history", [])
