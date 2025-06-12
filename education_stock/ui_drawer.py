# ui_drawer.py
import time
import pygame
import os
import math
from constants import LAYOUT, TICKERS
from font_loader import font
from data_loader import prices_by_ticker, volumes_by_ticker, dates_by_ticker, ipo_dates_by_ticker, current_prices_usd
import game_state
from utils import draw_text
from candle_chart import draw_candle_chart
from events import get_events_for_date, get_persistent_events
from save_manager import list_saved_files, load_game, save_game, delete_game
from game_state import game_mode, load_file_buttons, selected_save_file
from game_state import simulation_date_list, current_day_index, day_duration, day_start_time
from constants import LAYOUT
from constants import TICKERS

FONT = pygame.font.SysFont("Arial", 22)

selection_colors = [
    (0, 102, 255), (0, 204, 102), (255, 102, 102), (153, 102, 255),
]


def draw_date_and_timer(screen):
    if game_state.current_day_index >= len(game_state.simulation_date_list):
        return

    current_date = game_state.simulation_date_list[game_state.current_day_index]
    
    try:
        remaining = max(0, int(game_state.day_duration - (time.time() - game_state.day_start_time)))
    except AttributeError:
        remaining = 0

    font_large = pygame.font.SysFont("Arial", 28)
    date_text = f"📅 Date: {current_date.strftime('%Y-%m-%d')}"
    timer_text = f" ⏳ Next Day In: {remaining} sec"

    # 두 텍스트를 이어서 표시하기 위해 크기 측정
    date_label = font_large.render(date_text, True, (255, 255, 255))
    timer_label = font_large.render(timer_text, True, (255, 255, 0))

    x = 800
    y = 10

    # 그림자 효과 (검은 테두리)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            screen.blit(font_large.render(date_text, True, (0, 0, 0)), (x + dx, y + dy))
            screen.blit(font_large.render(timer_text, True, (0, 0, 0)), (x + dx + date_label.get_width(), y + dy))

    # 실제 텍스트
    screen.blit(date_label, (x, y))
    screen.blit(timer_label, (x + date_label.get_width(), y))



def draw_text(text, x, y, color, screen):
    label = FONT.render(text, True, color)
    screen.blit(label, (x, y))

def draw_main_menu(screen):
    screen.fill((20, 20, 20))
    width, height = screen.get_size()

    # 중앙 기준 위치
    center_x = width // 2
    top_y = height // 2 - 100

    title = "📊 Stock Game Menu"
    title_surface = FONT.render(title, True, (255, 255, 255))
    screen.blit(title_surface, (center_x - title_surface.get_width() // 2, top_y))

    new_game_btn = pygame.Rect(center_x - 100, top_y + 60, 200, 50)
    load_game_btn = pygame.Rect(center_x - 100, top_y + 130, 200, 50)

    pygame.draw.rect(screen, (100, 200, 100), new_game_btn)
    pygame.draw.rect(screen, (100, 100, 200), load_game_btn)

    draw_text("New Game", new_game_btn.x + 50, new_game_btn.y + 15, (0, 0, 0), screen)
    draw_text("Load Game", load_game_btn.x + 50, load_game_btn.y + 15, (0, 0, 0), screen)

    if selected_save_file:
        draw_text(f"Selected: {selected_save_file}", center_x - 100, load_game_btn.y + 60, (255, 255, 0), screen)

    return {"new": new_game_btn, "load": load_game_btn}

def draw_load_file_buttons(screen):
    screen.fill((30, 30, 30))
    draw_text("💾 Load Saved Game", 100, 40, (255, 255, 255), screen)

    files = list_saved_files()
    load_file_buttons.clear()
    start_y = 100

    for i, file in enumerate(files):
        y = start_y + i * 50
        file_rect = pygame.Rect(100, y, 300, 40)
        load_btn = pygame.Rect(420, y, 80, 40)
        del_btn = pygame.Rect(510, y, 80, 40)

        pygame.draw.rect(screen, (50, 50, 50), file_rect)
        pygame.draw.rect(screen, (0, 120, 255), load_btn)
        pygame.draw.rect(screen, (200, 50, 50), del_btn)

        draw_text(file, 110, y + 10, (255, 255, 255), screen)
        draw_text("Load", 430, y + 10, (255, 255, 255), screen)
        draw_text("Delete", 515, y + 10, (255, 255, 255), screen)

        load_file_buttons.append((file, load_btn, del_btn))

def is_stock_listed(ticker, current_date):
    ipo_date = ipo_dates_by_ticker.get(ticker)
    return ipo_date is not None and current_date >= ipo_date

def draw_ui(screen):
    screen.fill((0, 0, 0))
    current_date = game_state.simulation_date_list[game_state.current_day_index]

    game_state.visible_tickers = [
        ticker for ticker in TICKERS if is_stock_listed(ticker, current_date)
    ]

    if game_state.zoom_comparison_mode:
        draw_comparison_charts_zoomed(screen)
    elif game_state.comparison_mode and game_state.comparison_tickers:
        draw_comparison_charts_candlestick(screen)
    else:
        if is_stock_listed(game_state.current_ticker, current_date):
            draw_candle_image(screen, game_state.current_ticker, game_state.time_indices[game_state.current_ticker])

    draw_buttons(screen)
    draw_portfolio(screen)
    draw_total_profit(screen, game_state.time_indices)
    draw_alerts(screen, game_state.alerts)
    draw_news_history(screen, current_date)
    draw_longterm_news(screen, current_date)
    draw_comparison_button(screen)
    draw_selected_tickers(screen)
    draw_clear_button(screen)
    draw_zoom_button(screen)
    draw_top_10_by_price(screen)
    draw_all_companies_grid(screen)
    draw_top_10_ranked_stocks(screen)  # ✅ 복구 완료
    draw_date_and_timer(screen)

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
    draw_text("🔍 Zoom Mode", rect.x + 10, rect.y + 10, (0, 0, 0), screen)

def draw_selected_tickers(screen):
    if not game_state.comparison_mode:
        return
    x = 400
    y = 10
    for i, ticker in enumerate(game_state.comparison_tickers):
        color = selection_colors[i % len(selection_colors)]
        label = TICKERS.get(ticker, ticker)
        draw_text(f"{i+1}. {label}", x, y + i * 22, color, screen)

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
                label = TICKERS.get(ticker, ticker)
                draw_text(f"{label}: {qty} @ ${price:.2f}", x, y, (255, 255, 255), screen)
                y += LAYOUT["portfolio"]["line_height"]
            
            except Exception as e:
                print(f"📋 포트폴리오 표시 오류: {ticker} - {e}")

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

def draw_news_history(screen, current_date):
    if game_state.zoom_comparison_mode:
        return
    x, y = LAYOUT["news"]["x"] - 50, LAYOUT["news"]["y"]

    width, max_lines = LAYOUT["news"]["width"], LAYOUT["news"]["max_lines"]
    pygame.draw.rect(screen, (20, 20, 20), (x, y, width, max_lines * 20 + 10))
    draw_text("📰 News", x + 5, y + 5, (255, 255, 0), screen)
    latest_news = game_state.news_log[-max_lines:]
    for i, item in enumerate(latest_news):
        draw_text(item["message"], x + 5, y + 30 + i * 18, (255, 255, 255), screen)


def draw_longterm_news(screen, current_date):
    """뉴스 박스 아래에 Persistent Rumors를 독립적으로 표시"""
    # 뉴스 박스 기준 좌표 계산
    x = LAYOUT["news"]["x"] -50
    y = LAYOUT["news"]["y"] + LAYOUT["news"]["max_lines"] * 20 + 60  # 뉴스 박스 바로 아래로

    persistent_rumors = get_persistent_events(current_date)
    draw_text("📢 Persistent Rumors", x, y, (255, 200, 0), screen)

    if persistent_rumors:
        for i, line in enumerate(persistent_rumors):
            draw_text(line, x, y + 25 + i * 20, (255, 255, 255), screen)
    else:
        draw_text("No persistent rumors", x, y + 25, (150, 150, 150), screen)


def draw_top_10_by_price(screen):
    current_date = game_state.simulation_date_list[game_state.current_day_index]
    visible_prices = []
    game_state.top10_button_rects = {}
    for ticker in TICKERS:
        ipo = ipo_dates_by_ticker.get(ticker)
        if ipo and current_date >= ipo:
            usd_price = current_prices_usd.get(ticker)
            if usd_price:
                visible_prices.append((ticker, usd_price))

    sorted_by_price = sorted(visible_prices, key=lambda x: x[1], reverse=True)[:10]

    # ✅ 좌측 상단에 그리도록 위치 수정
    x, y = 20, 100
    draw_text("📈 Top 10 Prices", x, y - 30, (255, 255, 0), screen)

    for i, (ticker, price) in enumerate(sorted_by_price):
        rect = pygame.Rect(x, y + i * 35, 180, 30)
        game_state.top10_button_rects[ticker] = rect
        color = (0, 0, 255) if ticker == game_state.current_ticker else (230, 230, 230)
        pygame.draw.rect(screen, color, rect)
        text_color = (255, 255, 255) if color != (230, 230, 230) else (0, 0, 0)
        label = TICKERS.get(ticker, ticker)
        draw_text(f"{i+1}. {label}: ${price:.2f}", rect.x + 10, rect.y + 6, text_color, screen)


def draw_top_10_ranked_stocks(screen):
    current_date = game_state.simulation_date_list[game_state.current_day_index]
    profit_list = []
    for ticker, data in game_state.portfolio["stocks"].items():
        if not is_stock_listed(ticker, current_date):
            continue
        qty = data["quantity"]
        if qty <= 0:
            continue
        invested = qty * data["buy_price"]
        try:
            current_price = float(prices_by_ticker[f"{ticker}_Close"][game_state.time_indices[ticker]])
            current_value = qty * current_price
            profit = current_value - invested
            profit_list.append((ticker, profit))
        except:
            continue

    sorted_profit = sorted(profit_list, key=lambda x: x[1], reverse=True)[:10]

    # ✅ 위치: 포트폴리오 아래
    x = LAYOUT["portfolio"]["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x
    y = LAYOUT["portfolio"]["y_start"] + 200

    draw_text("🏆 Top 10 by Profit", x, y - 30, (255, 255, 0), screen)
    for i, (ticker, profit) in enumerate(sorted_profit):
        color = (255, 0, 0) if profit >= 0 else (0, 128, 255)
        label = TICKERS.get(ticker, ticker)
        draw_text(f"{i+1}. {label}: ${profit:.2f}", x, y + i * 25, color, screen)


def draw_all_companies_grid(screen):
    tickers = game_state.visible_tickers
    if not tickers:
        return
    max_rows = 5
    cell_width = 180
    cell_height = 40
    padding_x = 10
    padding_y = 8
    cols = math.ceil(len(tickers) / max_rows)
    start_x = 100
    start_y = LAYOUT["screen"]["height"] - (cell_height + padding_y) * max_rows - 20
    game_state.grid_button_rects = {}
    for i, ticker in enumerate(tickers):
        row = i % max_rows
        col = i // max_rows
        x = start_x + col * (cell_width + padding_x)
        y = start_y + row * (cell_height + padding_y)
        if ticker == game_state.current_ticker:
            color = (0, 128, 255)
        elif ticker in game_state.comparison_tickers:
            idx = game_state.comparison_tickers.index(ticker)
            color = selection_colors[idx % len(selection_colors)]
        else:
            color = (230, 230, 230)
        rect = pygame.Rect(x, y, cell_width, cell_height)
        game_state.grid_button_rects[ticker] = rect
        pygame.draw.rect(screen, color, rect)
        text_color = (0, 0, 0) if color == (230, 230, 230) else (255, 255, 255)
        label = TICKERS.get(ticker, ticker)
        draw_text(label, x + 10, y + 10, text_color, screen)

def draw_candle_image(screen, ticker, index):
    path = draw_candle_chart(ticker, prices_by_ticker, index)
    if os.path.exists(path):
        try:
            image = pygame.image.load(path)
            resized = pygame.transform.smoothscale(image, (900, 600))
            screen.blit(resized, (300, 50))
        except Exception as e:
            print("⚠️ 캔들 이미지 로딩 실패:", e)

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

def draw_loading_screen(screen, dot_count):
    screen.fill((10, 10, 10))
    loading_text = "LOADING" + "." * (dot_count % 6)  # 0~5 개수의 점 반복
    font_large = pygame.font.SysFont("Arial", 40)
    text_surface = font_large.render(loading_text, True, (255, 255, 255))
    x = screen.get_width() // 2 - text_surface.get_width() // 2
    y = screen.get_height() // 2 - text_surface.get_height() // 2
    screen.blit(text_surface, (x, y))
    pygame.display.flip()