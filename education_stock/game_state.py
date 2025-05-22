import datetime
import time
import pygame
import sys
from constants import TICKERS
from constants import LAYOUT
from ui_drawer import draw_ui
from data_loader import download_all_stock_data, prices_by_ticker, dates_by_ticker

# 전체 상태 변수들 정의
game_mode = "menu"
simulation_date_list = []
current_day_index = 0
current_ticker_index = 0
current_ticker = None
time_indices = {}
comparison_tickers = []
comparison_mode = False
comparison_zoom_mode = False
show_comparison_charts = False
chart_zoom_mode = False
chart_scroll_offset_index = 0
chart_zoom_scale = 1.0
chart_zoom_center_ratio = 0.5
scroll_offset = 0
MAX_SCROLL = 0

# 이벤트 관련
news_events = []
active_events = []

# 알림 및 입력
alerts = []
input_mode = None
input_text = ""
load_file_buttons = []
quantity_input_mode = False
quantity_input_text = ""
buy_quantity = 1

# 종목별 시점
first_available_date = {}

# 기타 전역 레이아웃 관련 스크롤
portfolio_scroll_offset = 0
PORTFOLIO_MAX_SCROLL = 0
stock_scroll_offset = 0
STOCK_MAX_SCROLL = 0

# ✅ 포트폴리오 상태 추가 (UI와 매매에서 사용함)
portfolio = {
    "cash": 100000.0,
    "stocks": {ticker: {"quantity": 0, "buy_price": 0.0} for ticker in prices_by_ticker.keys() if ticker.endswith("_Close")}
}

def init_game():
    global current_ticker, game_mode, simulation_date_list, time_indices, portfolio

    print("📱 데이터 다운로드 시작...")
    download_all_stock_data()

    # ✅ 포트폴리오 초기화 (데이터 다운로드 후에)
    portfolio = {
        "cash": 100000.0,
        "stocks": {
            ticker.replace("_Close", ""): {"quantity": 0, "buy_price": 0.0}
            for ticker in prices_by_ticker if ticker.endswith("_Close")
        }
    }

    # 날짜 리스트 구성
    for ticker, date_list in dates_by_ticker.items():
        if date_list:
            simulation_date_list = date_list
            print(f"📊 '{ticker}' 종목 기준으로 날짜 리스트 선택됨")
            break

    if not simulation_date_list:
        print("❌ 날짜 리스트 없음 → 게임 시작 불가")
        sys.exit()

    print(f"✅ 총 시룰리언 날짜 수: {len(simulation_date_list)}")
    print(f"📅 시작일: {simulation_date_list[0]}")
    print(f"📅 종료일: {simulation_date_list[-1]}")

    for ticker in dates_by_ticker:
        time_indices[ticker] = 0

    for key in prices_by_ticker:
        if key.endswith("_Close"):
            current_ticker = key.replace("_Close", "")
            break

    print(f"✅ 초기 종목: {current_ticker}")
    game_mode = "playing"


def main_loop():
    global current_day_index

    screen = pygame.display.set_mode((LAYOUT["screen"]["width"], LAYOUT["screen"]["height"]))
    pygame.display.set_caption("Stock Simulator")
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0,0,0))  # 흑 배경

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)   # ← 종목 변경
                handle_button_click(event.pos)  # ← Buy/Sell 버튼 처리

        # ✅ 날짜 진행 (1일씩)
        current_day_index += 1

        for ticker in time_indices:
            if time_indices[ticker] < len(dates_by_ticker[ticker]) - 1:
                time_indices[ticker] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)


        draw_ui(screen)
        pygame.display.flip()
        clock.tick(5)  # 초당 5일 진행

    pygame.quit()

def handle_mouse_click(pos):
    x, y = pos
    y_start = LAYOUT["stock_list"]["y_start"]
    for i, ticker in enumerate(list(TICKERS.keys())[:10]):
        rect = pygame.Rect(LAYOUT["stock_list"]["x"], y_start + i * 40, 150, 35)
        if rect.collidepoint(x, y):
            global current_ticker
            current_ticker = ticker
            alerts.append((f"Selected: {ticker}", time.time()))



from portfolio_manager import buy_stock, sell_stock

def handle_button_click(pos):
    x, y = pos
    buy_rect = pygame.Rect(
        LAYOUT["screen"]["width"] + LAYOUT["buttons"]["buy"]["offset_x"],
        LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - LAYOUT["buttons"]["buy"]["height"],
        LAYOUT["buttons"]["buy"]["width"],
        LAYOUT["buttons"]["buy"]["height"]
    )
    sell_rect = pygame.Rect(
        LAYOUT["screen"]["width"] + LAYOUT["buttons"]["sell"]["offset_x"],
        LAYOUT["screen"]["height"] - LAYOUT["buttons"]["offset_y"] - LAYOUT["buttons"]["sell"]["height"],
        LAYOUT["buttons"]["sell"]["width"],
        LAYOUT["buttons"]["sell"]["height"]
    )
    if buy_rect.collidepoint(x, y):
        buy_stock(current_ticker, 1)
    elif sell_rect.collidepoint(x, y):
        sell_stock(current_ticker, 1)

