import datetime
import time
import pygame
import sys
from constants import TICKERS, LAYOUT

from data_loader import download_all_stock_data, prices_by_ticker, dates_by_ticker, ipo_dates_by_ticker
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
news_log = []  # 📌 과거 뉴스 전체 저장용
screen = pygame.display.set_mode((2000, 1280)) 

def init_game():
    global simulation_date_list, current_ticker, time_indices, portfolio, game_mode

    print("📱 데이터 다운로드 시작...")
    simulation_date_list = download_all_stock_data(list(TICKERS.keys()))

    if not simulation_date_list:
        print("❌ 날짜 리스트 없음 → 게임 시작 불가")
        sys.exit()

    print(f"✅ 총 시루리언 날짜 수: {len(simulation_date_list)}")
    print(f"🗕️ 시작일: {simulation_date_list[0]}")
    print(f"🗕️ 종료일: {simulation_date_list[-1]}")

    # 초기 자사와 보유 주식 설정
    portfolio.update({
        "cash": 100000.0,
        "stocks": {ticker: {"quantity": 0, "buy_price": 0.0} for ticker in TICKERS}
    })

    time_indices.update({ticker: 0 for ticker in TICKERS})

    # 초기 티켓 선택 (IPO 보유한 중 가장 일정 다음일에 시작)
    for ticker in TICKERS:
        if is_stock_listed(ticker, simulation_date_list[0]):
            current_ticker = ticker
            break

    # 뉴스 이벤트 생성
    schedule_random_events(list(TICKERS.keys()), simulation_date_list, count=10)

    game_mode = "playing"

profit_history = []

def main_loop(screen):
    global current_day_index

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos)
                handle_button_click(event.pos)

        current_day_index += 1
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

        # ✅ UI 그리기
        from ui_drawer import draw_ui
        draw_ui(screen)

        pygame.display.flip()
        clock.tick(5)

def handle_mouse_click(pos):
    x, y = pos
    y_start = LAYOUT["stock_list"]["y_start"]
    current_date = simulation_date_list[current_day_index]
    
    for i, ticker in enumerate(visible_tickers):
        rect = pygame.Rect(LAYOUT["stock_list"]["x"], y_start + i * 40, 150, 35)
        if rect.collidepoint(x, y):
            global current_ticker
            current_ticker = ticker
            alerts.append((f"Selected: {ticker}", time.time()))
            break


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

def apply_news_events(current_date, current_index):
    events = get_events_for_date(current_date)
    for event in events:
        key = f"{event['ticker']}_Close"
        if key in prices_by_ticker and current_index < len(prices_by_ticker[key]):
            prices_by_ticker[key][current_index] *= (1 + event["impact"])
            alerts.append((event["message"], time.time()))
            print(f"📢 뉴스 적용: {event['ticker']} - {event['message']}")

def is_stock_listed(ticker, current_date):
    ipo_date = ipo_dates_by_ticker.get(ticker)
    return ipo_date is not None and current_date >= ipo_date

def apply_news_events(current_date, current_index):
    events = get_events_for_date(current_date)
    for event in events:
        key = f"{event['ticker']}_Close"
        if key in prices_by_ticker and current_index < len(prices_by_ticker[key]):
            prices_by_ticker[key][current_index] *= (1 + event["impact"])
            message = f"{current_date} - {event['message']}"
            alerts.append((event["message"], time.time()))
            news_log.append(message)  # ✅ 로그에 추가
            print(f"📢 뉴스 적용: {event['ticker']} - {event['message']}")
