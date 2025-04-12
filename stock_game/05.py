import yfinance as yf
import pygame
import time
import datetime
import sys
import json
import os

SAVE_DIR = "saves"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)


# ----- 1. 데이터 준비: 여러 종목 데이터 다운로드 -----
TICKERS = {
    'AAPL': 'Apple',
    'GOOG': 'Google',
    'TSLA': 'Tesla',
    'MSFT': 'Microsoft',
    'AMZN': 'Amazon',
    'META': 'Meta',
    'NFLX': 'Netflix',
    'NVDA': 'Nvidia',
    'INTC': 'Intel',
    'AMD': 'AMD',
    'DIS': 'Disney',
    'IBM': 'IBM',
    'ORCL': 'Oracle',
    'PYPL': 'PayPal',
    'ADBE': 'Adobe',
    'QCOM': 'Qualcomm',
    'KO': 'CocaCola'
}

LAYOUT = {
    "screen": {"width": 1366, "height": 768},
    "chart": {"x": 478, "y": 50, "width": 751, "height": 268},
    "buttons": {
        "buy": {"width": 136, "height": 45, "offset_x": -341},
        "sell": {"width": 136, "height": 45, "offset_x": -163},
        "offset_y": 15
    },
    "stock_list": {
        "x": 30, "y_start": 100, "button_height": 35, "visible_height": 300,
        "title_x": 30, "title_y": 60
    },
    "grid": {
        "x": 30, "y_offset_from_bottom": 10,
        "cols": 4, "rows": 4,
        "cell_width": 273, "cell_height": 35
    },
    "portfolio": {
        "x": -273, "y_start": 100, "visible_height": 400, "line_height": 25
    },
    "alerts": {"x": 614, "y_base": 668, "line_height": 20, "max": 3},
    "profit_summary": {"x": -273, "y": 10},
    "rank_chart": {
        "x_from_grid": True,
        "offset_from_grid_x": 40,
        "offset_y": -15,
        "width": 683,
        "extra_height": 20
    },
    "cash": {"x": 30, "y": 30}
}


COMPANY_COLORS = {
    'AAPL': (255, 99, 132),
    'GOOG': (54, 162, 235),
    'TSLA': (255, 206, 86),
    'MSFT': (75, 192, 192),
    'AMZN': (153, 102, 255),
    'META': (255, 159, 64),
    'NFLX': (199, 199, 199),
    'NVDA': (83, 102, 255),
    'INTC': (255, 99, 255),
    'AMD': (99, 255, 132),
    'DIS': (100, 100, 100),
    'IBM': (255, 70, 70),
    'ORCL': (0, 230, 115),
    'PYPL': (204, 204, 0),
    'ADBE': (0, 153, 153),
    'QCOM': (102, 0, 204),
    'KO': (255, 51, 0)
}
default_save_file = "autosave.json"

input_mode = None  # "save" or "load"
input_text = ""  # 현재 입력 중인 텍스트
load_file_buttons = []  # load 모드일 때 파일 선택 버튼 저장

back_to_menu_rect = pygame.Rect(20, 20, 100, 30)
load_back_button_rect = pygame.Rect(20, 20, 100, 30)

chart_zoom_mode = False
chart_zoom_scale = 1.0
chart_zoom_center_ratio = 0.5


all_company_buttons = []
portfolio_scroll_offset = 0
PORTFOLIO_SCROLL_STEP = 20
PORTFOLIO_MAX_SCROLL = 0
PORTFOLIO_SUMMARY_HEIGHT = 100  # 투자 총합, 현재 가치, 수익률 텍스트 높이


stock_scroll_offset = 0
STOCK_SCROLL_STEP = 20
STOCK_MAX_SCROLL = 0


prices_by_ticker = {}
dates_by_ticker = {}
first_available_date = {}  # 전역으로 선언해야 모든 함수에서 접근 가능
rank_history = {ticker: {} for ticker in TICKERS}  # 모든 티커에 대해 날짜별 순위 기록


start_date = "2000-01-01"  # 예: 2000년 1월 1일 부터
end_date = datetime.datetime.now().strftime("%Y-%m-%d")

current_day_index = 0  # 현재 시뮬레이션 날짜 인덱스
# 전역 변수 초기화
current_ticker_index = 0
current_ticker = list(TICKERS.keys())[0]
time_indices = {ticker: 0 for ticker in TICKERS}

scroll_offset = 0
MAX_SCROLL = 0  # 이후 버튼 길이에 따라 계산



for ticker in TICKERS:
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")['Close'].dropna()
    prices_by_ticker[ticker] = [float(p.item()) for p in stock_data.values]
    dates_by_ticker[ticker] = [dt.strftime("%y.%m.%d") for dt in stock_data.index]

    first_available_date[ticker] = stock_data.index[0].date()

simulation_date_list = sorted(set().union(*[dates_by_ticker[ticker] for ticker in dates_by_ticker]))
simulation_date_list = [datetime.datetime.strptime(d, "%y.%m.%d").date() for d in simulation_date_list]
simulation_date_list.sort() 

# ----- 2. 게임 상태 초기화 -----
game_state = "menu"  # "menu", "playing"


portfolio = {
    'cash': 100000,
    'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
}
alerts = []



# ----- 3. Pygame 초기화 및 화면 설정 -----
pygame.init()

# 화면 해상도 정보 가져오기
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# 💡 세로 모드일 경우에도 강제로 가로로 세팅
if screen_height > screen_width:
    screen_width, screen_height = 1400, 700

# 작업표시줄과 타이틀바가 보이도록 화면에서 살짝 작게 설정 (예: -50 픽셀씩 줄임)
margin_x, margin_y = 50, 50
window_width = screen_width - margin_x
window_height = screen_height - margin_y



# 윈도우 타이틀과 닫기 버튼이 보이게 유지하기 위해 RESIZABLE 플래그 사용
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

# LAYOUT에도 반영하여 나머지 UI가 자동으로 조정됨
LAYOUT["screen"]["width"], LAYOUT["screen"]["height"] = window_width, window_height


pygame.display.set_caption("Stock Trading Simulator")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

current_ticker_index = 0
time_indices = {ticker: 0 for ticker in TICKERS}




# 주식 목록 버튼 정의
# ✅ 대체할 새로운 버튼 생성 코드
button_height = 40  # 버튼 높이 설정
stock_buttons = []
for i, ticker in enumerate(TICKERS):
    rect = pygame.Rect(50, 100 + i * button_height, 150, button_height)
    stock_buttons.append((ticker, rect))  # (티커, 위치정보) 튜플로 저장

# ✅ 스크롤 최대 거리 계산 (아래 공간이 500 픽셀 기준일 때)
MAX_SCROLL = max(0, len(TICKERS) * button_height - 500)


# ----- 4. 함수 정의 -----
def save_game(filename=None):
    try:
        if filename is None:
            filename = default_save_file
            if not filename.endswith(".json"):
                filename += ".json"

        # ✅ 저장 경로 구성
        filepath = os.path.join(SAVE_DIR, filename)
        temp_filename = filepath + ".tmp"

        recent_days = simulation_date_list[max(0, current_day_index - 100): current_day_index + 1]
        rank_history_trimmed = {
            t: {str(day): rank for day, rank in ranks.items() if day in recent_days}
            for t, ranks in rank_history.items()
        }

        save_data = {
            "portfolio": portfolio,
            "current_day_index": current_day_index,
            "time_indices": time_indices,
            "current_ticker": current_ticker,
            "rank_history": rank_history_trimmed
        }

        with open(temp_filename, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=2)
        os.replace(temp_filename, filepath)

        alerts.append((f"{filename} 저장 완료", time.time()))
        print(f"[Saved] {filepath}")
    except Exception as e:
        alerts.append((f"저장 오류: {str(e)}", time.time()))
        print("저장 중 오류 발생:", e)


def load_game(filename=None):
    global portfolio, current_day_index, time_indices, current_ticker, rank_history, game_state

    try:
        if filename is None:
            save_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
            if not save_files:
                alerts.append(("⚠ 저장된 파일이 없습니다.", time.time()))
                return
            
            print("📂 저장된 파일 목록:")
            for i, f in enumerate(save_files):
                print(f"{i+1}. {f}")
            choice = int(input("불러올 번호 선택: ")) - 1
            filename = save_files[choice]

        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            portfolio = data["portfolio"]
            current_day_index = data["current_day_index"]
            time_indices = data["time_indices"]
            current_ticker = data["current_ticker"]

            raw_rank_history = data["rank_history"]
            rank_history = {}
            for ticker, ranks in raw_rank_history.items():
                rank_history[ticker] = {
                    datetime.datetime.strptime(date_str, "%Y-%m-%d").date(): rank
                    for date_str, rank in ranks.items()
                }

        alerts.append((f"{filename} 불러오기 완료", time.time()))
        game_state = "playing"  # <-- 게임 화면으로 전환


    except Exception as e:
        print("게임 불러오기 오류:", e)



def draw_load_file_buttons():
    global load_file_buttons
    load_file_buttons = []

    # 🔙 뒤로가기 버튼
    pygame.draw.rect(screen, (150, 150, 150), load_back_button_rect)
    draw_text("← Menu", load_back_button_rect.x + 10, load_back_button_rect.y + 5)

    save_files = [f for f in os.listdir(SAVE_DIR) if f.endswith(".json")]
    start_y = 160
    for i, fname in enumerate(save_files):
        btn_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 150, start_y + i * 45, 300, 40)
        pygame.draw.rect(screen, (70, 70, 70), btn_rect)
        pygame.draw.rect(screen, (255, 255, 255), btn_rect, 2)
        draw_text(fname, btn_rect.x + 10, btn_rect.y + 10)
        
        delete_rect = pygame.Rect(btn_rect.right + 10, btn_rect.y, 80, btn_rect.height)
        pygame.draw.rect(screen, (200, 50, 50), delete_rect)
        draw_text("Delete", delete_rect.x + 5, delete_rect.y + 10)

        load_file_buttons.append((fname, btn_rect, delete_rect))


def get_layout_x(key):
    x = LAYOUT[key]["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x
    return x


def adjust_layout_for_orientation():
    return  # <- 아무것도 안 하게 만들기


def draw_buttons(prev_y):
    button_layout = LAYOUT["buttons"]
    screen_width = LAYOUT["screen"]["width"]

    # offset_x가 음수일 경우 오른쪽 정렬
    buy_x = screen_width + button_layout["buy"]["offset_x"]
    sell_x = screen_width + button_layout["sell"]["offset_x"]
    button_y = prev_y + 10

    buy_rect = pygame.Rect(buy_x, button_y, button_layout["buy"]["width"], button_layout["buy"]["height"])
    sell_rect = pygame.Rect(sell_x, button_y, button_layout["sell"]["width"], button_layout["sell"]["height"])

    pygame.draw.rect(screen, (70, 130, 180), buy_rect)
    pygame.draw.rect(screen, (180, 70, 70), sell_rect)

    screen.blit(font.render("Buy", True, (255, 255, 255)), (buy_rect.x + 50, buy_rect.y + 15))
    screen.blit(font.render("Sell", True, (255, 255, 255)), (sell_rect.x + 50, sell_rect.y + 15))

    return buy_rect, sell_rect



def draw_chart(prices, dates):
    # 차트 위치와 크기를 LAYOUT에서 가져옴
    chart_layout = LAYOUT["chart"]
    offset_x = chart_layout["x"]
    offset_y = chart_layout["y"]
    width = chart_layout["width"]
    height = chart_layout["height"]

    if len(prices) < 2:
        return

    draw_text(f"Stock Chart: {TICKERS[current_ticker]} ({current_ticker})", offset_x, offset_y - 30, (255, 255, 0))
    
    prices = [float(p) for p in prices]
    max_price = max(prices)
    min_price = min(prices)
    scale = height / (max_price - min_price) if max_price != min_price else 1

    # --- 1. Y축 (가격) 눈금 ---
    price_range = max_price - min_price
    num_horizontal = min(max(int(price_range // 10), 4), 10)
    price_step = price_range / num_horizontal

    for i in range(num_horizontal + 1):
        y_line = offset_y + i * (height / num_horizontal)
        pygame.draw.line(screen, (80, 80, 80), (offset_x, y_line), (offset_x + width, y_line), 1)
        price_tick = max_price - i * price_step
        draw_text(f"${price_tick:.2f}", offset_x - 60, y_line - 10, (200, 200, 200))

    # --- 2. X축 (날짜) 눈금 ---
    num_vertical = 6
    for j in range(num_vertical + 1):
        x_line = offset_x + j * (width / num_vertical)
        pygame.draw.line(screen, (80, 80, 80), (x_line, offset_y), (x_line, offset_y + height), 1)
        index = int(j * (len(dates) - 1) / num_vertical)
        date_label = dates[index]
        draw_text(date_label[:7], x_line - 25, offset_y + height + 5, (200, 200, 200))

    # --- 3. 주가 선 그래프 ---
    points = []
    for i, price in enumerate(prices):
        x_point = offset_x + i * (width / (len(prices) - 1))
        y_point = offset_y + height - (price - min_price) * scale
        points.append((float(x_point), float(y_point)))

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)


def draw_portfolio_summary():
    portfolio_layout = LAYOUT["portfolio"]
    screen_height = LAYOUT["screen"]["height"]
    button_height = LAYOUT["buttons"]["buy"]["height"]
    button_offset_y = LAYOUT["buttons"]["offset_y"]

    # 버튼이 있는 위치보다 위에서만 보여지도록 제한
    max_visible_bottom = screen_height - button_height - button_offset_y - 20
    visible_height = max_visible_bottom - portfolio_layout["y_start"]

    x = portfolio_layout["x"]
    if x < 0:
        x = LAYOUT["screen"]["width"] + x

    y_start = portfolio_layout["y_start"]
    y = y_start - portfolio_scroll_offset
    line_height = portfolio_layout["line_height"]
    total_items = 0

    draw_text("Portfolio", x, y - 40, (255, 255, 0))

    total_invested = 0.0
    total_current_value = 0.0

    for ticker, data in portfolio["stocks"].items():
        quantity = data["quantity"]
        if quantity == 0:
            continue

        if y > max_visible_bottom:
            break  # 화면 아래로 넘어가면 출력 중단

        index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
        current_price = float(prices_by_ticker[ticker][index])
        avg_price = data["buy_price"]
        profit_percent = ((current_price - avg_price) / avg_price) * 100
        color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)
        company_name = TICKERS[ticker]

        draw_text(f"{company_name} ({ticker})", x, y, (255, 255, 255))
        draw_text(f"{quantity}주 @ {avg_price:.2f}", x, y + 15, (200, 200, 200))
        draw_text(f"{profit_percent:+.2f}%", x + 150, y + 15, color)

        y += line_height + 10
        total_items += 1

        total_invested += quantity * avg_price
        total_current_value += quantity * current_price

    # 수익 계산
    if total_invested > 0:
        total_profit = total_current_value - total_invested
        profit_percent = (total_profit / total_invested) * 100
    else:
        total_profit = 0
        profit_percent = 0

    color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)

    y += 20
    if y <= max_visible_bottom:
        draw_text(f"Total Invested: ${total_invested:.2f}", x, y, (255, 255, 255))
        draw_text(f"Current Value: ${total_current_value:.2f}", x, y + 20, (255, 255, 255))
        draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y + 40, color)

    # 스크롤 계산
    content_height = (total_items * (line_height + 10)) + 100
    global PORTFOLIO_MAX_SCROLL
    PORTFOLIO_MAX_SCROLL = max(0, content_height - visible_height)

    return y + 70


def cash():
    x = LAYOUT["cash"]["x"]
    y = LAYOUT["cash"]["y"]
    draw_text(f"Cash: ${float(portfolio['cash']):.2f}", x, y)


def draw_all_companies_grid():
    today = simulation_date_list[current_day_index]
    visible_companies = [ticker for ticker in TICKERS if first_available_date[ticker] <= today]

    visible_companies.sort(key=lambda t: first_available_date[t])
    
    grid_x = LAYOUT["grid"]["x"]
    cell_width = LAYOUT["grid"]["cell_width"]
    cell_height = LAYOUT["grid"]["cell_height"]
    cols = LAYOUT["grid"]["cols"]
    rows = LAYOUT["grid"]["rows"]

    grid_height = cell_height * rows
    grid_y = LAYOUT["screen"]["height"] - grid_height - LAYOUT["grid"]["y_offset_from_bottom"]

    all_company_buttons.clear()

    total_cells = cols * rows

    for idx in range(total_cells):
        col = idx % cols
        row = idx // cols
        x = grid_x + col * cell_width
        y = grid_y + row * cell_height

        rect = pygame.Rect(x, y, cell_width, cell_height)

        if idx < len(visible_companies):
            ticker = visible_companies[idx]
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)
            draw_text(f"{TICKERS[ticker]} ({ticker})", x + 5, y + 10)
            all_company_buttons.append((ticker, rect))
        else:
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)


def draw_stock_list(visible_companies):
    draw_text("Current Stock Rankings", LAYOUT["stock_list"]["title_x"], LAYOUT["stock_list"]["title_y"], (255, 255, 0))
    today = simulation_date_list[current_day_index]

    current_prices = []
    for ticker in visible_companies:
        index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
        current_price = prices_by_ticker[ticker][index]
        current_prices.append((ticker, current_price))
    
    current_prices.sort(key=lambda x: x[1], reverse=True)

    stock_buttons.clear()
    top_10 = current_prices[:10]  # ✅ 10개만 잘라서 보여줌

    for rank, (ticker, price) in enumerate(top_10, start=1):
        rect = pygame.Rect(50, 100 + len(stock_buttons) * button_height, 250, button_height)
        stock_buttons.append((ticker, rect, rank, price))

    # ✅ 여기를 아래로 이동
    rank_today = {ticker: rank for rank, (ticker, _) in enumerate(current_prices, start=1)}
    for ticker in rank_today:
        rank_history[ticker][today] = rank_today[ticker]

    for ticker, rect, rank, price in stock_buttons:
        shifted_rect = pygame.Rect(rect.x, rect.y - stock_scroll_offset, rect.width, rect.height)
        pygame.draw.rect(screen, (100, 100, 100), shifted_rect)
        text = font.render(f"{rank}. {TICKERS[ticker]} ({ticker}) - ${price:.2f}", True, (255, 255, 255))
        screen.blit(text, (shifted_rect.x + 10, shifted_rect.y + 5))

    # 스크롤 최대 거리 계산
    global STOCK_MAX_SCROLL
    STOCK_MAX_SCROLL = max(0, len(top_10) * button_height - 400)



def draw_text(text, x, y, color=(255, 255, 255)):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_input_box():
    global input_text
    box_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 150, 100, 300, 40)
    pygame.draw.rect(screen, (255, 255, 255), box_rect)
    pygame.draw.rect(screen, (0, 0, 0), box_rect, 2)
    draw_text(input_text, box_rect.x + 10, box_rect.y + 10, (0, 0, 0))

    # 🔙 뒤로가기 버튼
    pygame.draw.rect(screen, (150, 150, 150), load_back_button_rect)
    draw_text("← Menu", load_back_button_rect.x + 10, load_back_button_rect.y + 5)



def update_data():
    global prices_by_ticker, dates_by_ticker
    # 예시: 각 티커별로 오늘 날짜부터 현재까지 1분 단위 데이터를 업데이트
    first_available_date = {}

    for ticker in TICKERS:
        stock_data = yf.download(ticker, start=start_date, end=end_date, interval="1d")['Close'].dropna()
        prices_by_ticker[ticker] = [float(p.item()) for p in stock_data.values]
        dates_by_ticker[ticker] = [dt.strftime("%y.%m.%d") for dt in stock_data.index]

        first_available_date[ticker] = stock_data.index[0].date()

        # ✅ 최초 날짜 저장
        first_date = stock_data.index[0].date()  # datetime.date 객체로 저장
        first_available_date[ticker] = first_date

def update_intraday_data():
    # 최신 1일치 인트라데이 데이터를 가져오는 예제
    global prices_by_ticker, dates_by_ticker
    for ticker in TICKERS:
        stock_data = yf.download(ticker, period="1d", interval="1m")['Close'].dropna()
        prices_by_ticker[ticker] = [float(p) for p in list(stock_data.values)]
        dates_by_ticker[ticker] = [dt.strftime("%H:%M") for dt in stock_data.index]

        first_available_date[ticker] = stock_data.index[0].date()

def buy_stock(ticker):
    global alerts
    index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)  # 🔐 인덱스 보호
    price = float(prices_by_ticker[ticker][index])
    if portfolio['cash'] >= price:
        portfolio['cash'] -= price
        info = portfolio['stocks'][ticker]
        total_cost = info['quantity'] * info['buy_price'] + price
        info['quantity'] += 1
        info['buy_price'] = total_cost / info['quantity']
        alerts.append((f"Bought 1 {ticker}", time.time()))
    else:
        alerts.append((f"Not enough cash to buy {ticker}", time.time()))

def sell_stock(ticker):
    global alerts
    index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)  # 🔐 인덱스 보호
    price = float(prices_by_ticker[ticker][index])
    info = portfolio['stocks'][ticker]
    if info['quantity'] > 0:
        price = float(prices_by_ticker[ticker][time_indices[ticker]])
        portfolio['cash'] += price
        info['quantity'] -= 1
        alerts.append((f"Sold 1 {ticker}", time.time()))
        if info['quantity'] == 0:
            info['buy_price'] = 0
    else:
        alerts.append((f"No {ticker} to sell", time.time()))

def draw_alerts():
    now = time.time()
    duration = 1.5  # 초단위, 몇 초 동안 보여줄지

    # 오래된 메시지 제거
    alerts[:] = [entry for entry in alerts if now - entry[1] <= duration]

    # 최근 메시지 3개만 보여줌
    for i, (msg, _) in enumerate(alerts[-3:]):
        x = LAYOUT["alerts"]["x"]
        y_base = LAYOUT["alerts"]["y_base"]
        line_height = LAYOUT["alerts"]["line_height"]
        draw_text(msg, x, y_base + i * line_height, (255, 255, 0))



def draw_rank_chart(rank_history, offset_x, offset_y, width, height):
    if not rank_history:
        return

    tickers = list(rank_history.keys())
    date_list = sorted(list({date for ranks in rank_history.values() for date in ranks.keys()}))
    num_dates = len(date_list)

    if num_dates <= 1:
        return  # 날짜가 1개 이하일 땐 그래프 그리지 않음
    
    max_rank = max(len(tickers), 10)
    scale_x = width / (num_dates - 1)
    scale_y = height / max_rank

    # 회사별 순위 그래프 그리기
    for ticker in tickers:
        points = []
        for i, date in enumerate(date_list):
            rank = rank_history[ticker].get(date, None)
            if rank is None:
                continue
            x = offset_x + i * scale_x
            y = offset_y + (rank - 1) * scale_y
            points.append((x, y))
        
        # 회사별 고유 색상 사용, 굵은 선으로 표현
        if len(points) >= 2:
            color = COMPANY_COLORS.get(ticker, (255, 255, 255))
            pygame.draw.lines(screen, color, False, points, 3)

        # 그래프 오른쪽 끝에 회사명 표시 (선 끝에)
        if points:
            last_x, last_y = points[-1]
            draw_text(TICKERS[ticker], last_x + 5, last_y - 10, color)

    # X축 눈금(날짜) 추가 표시
    for i, date in enumerate(date_list):
        if i % max(1, num_dates // 10) == 0 or i == num_dates - 1:
            x = offset_x + i * scale_x
            draw_text(date.strftime("%y-%m-%d"), x - 20, offset_y + height + 5, (200, 200, 200))

    # Y축 눈금(순위) 라벨 표시
    for r in range(1, max_rank + 1):
        y_line = offset_y + (r - 1) * scale_y
        draw_text(f"{r}위", offset_x - 40, y_line - 10, (200, 200, 200))


def draw_total_profit():
    total_invested = 0.0
    total_current_value = 0.0

    for ticker, data in portfolio["stocks"].items():
        quantity = data["quantity"]
        if quantity > 0:
            invested = quantity * data["buy_price"]
            current_price = float(prices_by_ticker[ticker][time_indices[ticker]])
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

    draw_text(f"Total Invested: ${total_invested:.2f}", x, y, (255, 255, 255))
    draw_text(f"Current Value: ${total_current_value:.2f}", x, y + 20, (255, 255, 255))
    draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y + 40, color)


def get_sorted_visible_stocks():
    today = simulation_date_list[current_day_index]
    visible = []

    for ticker in TICKERS:
        if first_available_date[ticker] <= today:
            quantity = portfolio["stocks"][ticker]["quantity"]
            price_index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
            current_price = prices_by_ticker[ticker][price_index]
            total_value = quantity * current_price
            visible.append((ticker, total_value))

    # 가치 기준 정렬 (내림차순)
    visible.sort(key=lambda x: -x[1])
    return visible

def get_rank_chart_position():
    grid = LAYOUT["grid"]
    chart = LAYOUT["rank_chart"]
    grid_x = grid["x"]
    grid_cols = grid["cols"]
    cell_width = grid["cell_width"]
    grid_height = grid["cell_height"] * grid["rows"]
    grid_y = LAYOUT["screen"]["height"] - grid_height - grid["y_offset_from_bottom"]

    x = grid_x + (cell_width * grid_cols) + chart["offset_from_grid_x"]
    y = grid_y + chart["offset_y"]
    width = chart["width"]
    height = grid_height + chart["extra_height"]
    return x, y, width, height
def draw_zoomed_chart(prices, dates):
    screen.fill((0, 0, 0))
    offset_x, offset_y = 80, 80
    width = LAYOUT["screen"]["width"] - 160
    height = 400

    total_len = len(prices)
    view_len = int(total_len * chart_zoom_scale)
    center_index = int(total_len * chart_zoom_center_ratio)
    start = max(0, center_index - view_len // 2)
    end = min(total_len, start + view_len)

    prices_view = prices[start:end]
    dates_view = dates[start:end]
    if len(prices_view) < 2:
        return

    max_price = max(prices_view)
    min_price = min(prices_view)
    scale = height / (max_price - min_price) if max_price != min_price else 1

    # Y축 눈금
    for i in range(5):
        y = offset_y + i * height / 4
        val = max_price - i * (max_price - min_price) / 4
        pygame.draw.line(screen, (60, 60, 60), (offset_x, y), (offset_x + width, y))
        draw_text(f"${val:.2f}", offset_x - 60, y - 10, (200, 200, 200))

    # X축 눈금
    for i in range(6):
        x = offset_x + i * width / 5
        idx = int(i * (len(dates_view) - 1) / 5)
        label = dates_view[idx][:7]
        pygame.draw.line(screen, (60, 60, 60), (x, offset_y), (x, offset_y + height))
        draw_text(label, x - 25, offset_y + height + 5, (200, 200, 200))

    # 라인 그래프
    points = []
    for i, p in enumerate(prices_view):
        x = offset_x + i * width / (len(prices_view) - 1)
        y = offset_y + height - (p - min_price) * scale
        points.append((x, y))

    pygame.draw.lines(screen, (0, 255, 0), False, points, 2)
    draw_text("ESC to exit zoom", offset_x, offset_y + height + 40, (255, 255, 255))


def draw_ui():
    today = simulation_date_list[current_day_index]
    visible_companies = [ticker for ticker in TICKERS if first_available_date[ticker] <= today]
    draw_stock_list(visible_companies)
    cash()
    draw_alerts()
    y_after_profit = draw_portfolio_summary()
    global buy_button_rect, sell_button_rect
    buy_button_rect, sell_button_rect = draw_buttons(y_after_profit)
    draw_all_companies_grid()

    # 주가 차트
    if current_ticker in prices_by_ticker and simulation_date_list[current_day_index] >= first_available_date[current_ticker]:
        current_index = min(time_indices[current_ticker], len(prices_by_ticker[current_ticker]) - 1)
        prices = prices_by_ticker[current_ticker][:max(2, current_index + 1)]
        dates = dates_by_ticker[current_ticker][:max(2, current_index + 1)]

        draw_chart(prices, dates)
        # 순위 그래프
        rank_x, rank_y, rank_w, rank_h = get_rank_chart_position()
        draw_rank_chart(rank_history, offset_x=rank_x, offset_y=rank_y, width=rank_w, height=rank_h)
    
    # 🟡 뒤로가기 버튼
    pygame.draw.rect(screen, (150, 150, 150), back_to_menu_rect)
    draw_text("← Menu", back_to_menu_rect.x + 10, back_to_menu_rect.y + 5)

def draw_main_menu():
    screen.fill((20, 20, 20))
    title = font.render(" stock simulator", True, (255, 255, 0))
    screen.blit(title, (LAYOUT["screen"]["width"] // 2 - 100, 100))

    global menu_new_game_rect, menu_continue_rect
    menu_new_game_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 100, 200, 200, 50)
    menu_continue_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 100, 270, 200, 50)

    pygame.draw.rect(screen, (70, 130, 180), menu_new_game_rect)
    pygame.draw.rect(screen, (100, 100, 100), menu_continue_rect)

    screen.blit(font.render("new game start", True, (255, 255, 255)), (menu_new_game_rect.x + 30, menu_new_game_rect.y + 15))
    screen.blit(font.render("load game", True, (255, 255, 255)), (menu_continue_rect.x + 50, menu_continue_rect.y + 15))

    if input_mode == "load":
        draw_load_file_buttons()  # 🔥 여기에 명시적으로 강제 추가




# ----- 5. 메인 루프 -----
running = True
while running:
    screen.fill((30, 30, 30))

    today = simulation_date_list[current_day_index]
    visible_companies = [ticker for ticker in TICKERS if first_available_date[ticker] <= today]

    

    for event in pygame.event.get():
        if input_mode == "save" and event.type == pygame.MOUSEBUTTONDOWN:
            if load_back_button_rect.collidepoint(event.pos):
                input_mode = None
                input_text = ""
                continue


        if event.type == pygame.QUIT:
            running = False
    
        # 🔹 저장 파일 클릭 처리 (load 모드일 때)
        if input_mode == "load" and event.type == pygame.MOUSEBUTTONDOWN:
    # 🔹 확대 모드는 load/save 모드에서는 무시
            if input_mode is None:
                chart_rect = pygame.Rect(LAYOUT["chart"]["x"], LAYOUT["chart"]["y"], LAYOUT["chart"]["width"], LAYOUT["chart"]["height"])
                if chart_rect.collidepoint(event.pos):
                    chart_zoom_mode = True
                    chart_zoom_scale = 1.0
                    rel_x = event.pos[0] - chart_rect.x
                    chart_zoom_center_ratio = rel_x / chart_rect.width


            # 🔙 먼저 뒤로가기 버튼부터 체크!
            if load_back_button_rect.collidepoint(event.pos):
                            input_mode = None
                            input_text = ""
                            continue
            
            for fname, load_rect, del_rect in load_file_buttons:
                if del_rect.collidepoint(event.pos):
                    try:
                        os.remove(os.path.join(SAVE_DIR, fname))
                        alerts.append((f"{fname} 삭제됨", time.time()))
                        draw_load_file_buttons()  # 목록 새로고침
                    except Exception as e:
                        alerts.append((f"삭제 실패: {e}", time.time()))
                    break
                
                elif load_rect.collidepoint(event.pos):
                    load_game(fname)
                    input_mode = None
                    input_text = ""
                    break
            continue
            
            # 저장파일 버튼 체크
            
        
        # 🔹 저장 파일명 입력 처리 (save 모드일 때)
        if chart_zoom_mode and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # 휠 위
                chart_zoom_scale = max(0.1, chart_zoom_scale - 0.1)
            elif event.button == 5:  # 휠 아래
                chart_zoom_scale = min(2.0, chart_zoom_scale + 0.1)

            
            if event.key == pygame.K_BACKSPACE:
                input_mode = None
                input_text = ""
            if event.key == pygame.K_RETURN: 
                filename = input_text.strip()

                # 🔽 파일명이 비어있으면 저장하지 않음
                if not filename:
                    alerts.append(("파일명을 입력하세요", time.time()))
                    continue
                
                # 🔽 .json 확장자 없으면 자동 추가
                if not filename.endswith(".json"):
                    filename += ".json"

                save_game(filename)
                input_mode = None
                input_text = ""

            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode
            continue  # save 모드에서도 다른 이벤트 무시
        
        elif event.type == pygame.KEYDOWN:
            if chart_zoom_mode:
                if event.key == pygame.K_ESCAPE:
                    chart_zoom_mode = False
                continue
            
            # 🔽 여기부터 추가해줘 (save 모드에서 키보드 입력 받기)
            if input_mode == "save":
                if event.key == pygame.K_RETURN:
                    filename = input_text.strip()
                    if not filename.endswith(".json"):
                        filename += ".json"
                    save_game(filename)
                    input_mode = None
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
                continue  # 다른 키 이벤트 무시


            if chart_zoom_mode:
                if event.key == pygame.K_ESCAPE:
                    chart_zoom_mode = False
                continue
            
            # 다른 이름 저장 (Shift + S)
            if event.key == pygame.K_s:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    input_mode = "save"
                    input_text = ""
                else:
                    save_game()
                continue

            
            # 단순 저장 (S만 눌렀을 때)
            if event.key == pygame.K_s:
                save_game()  # default_save_file 사용
                continue
            
            # 일반 키 입력
            if event.key == pygame.K_s:
                input_mode = "save"
                input_text = ""
            elif event.key == pygame.K_l:
                input_mode = "load"
                input_text = ""

    
        # 🔹 마우스 클릭 처리 (메뉴 or 게임 중일 때)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "menu":
                if menu_new_game_rect.collidepoint(event.pos):
                    game_state = "playing"
                    current_day_index = 0
                    portfolio = {
                        'cash': 100000,
                        'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
                    }
                elif menu_continue_rect.collidepoint(event.pos):
                    input_mode = "load"
                continue

            if chart_zoom_mode:
                pressed = pygame.mouse.get_pressed()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # 휠 위
                        chart_zoom_scale = max(0.1, chart_zoom_scale - 0.1)
                    elif event.button == 5:  # 휠 아래
                        chart_zoom_scale = min(2.0, chart_zoom_scale + 0.1)



            elif game_state == "playing":
                if event.button == 4:  # 마우스 휠 위
                    scroll_offset = max(0, scroll_offset - 20)
                    portfolio_scroll_offset = max(0, portfolio_scroll_offset - PORTFOLIO_SCROLL_STEP)
                    stock_scroll_offset = max(0, stock_scroll_offset - STOCK_SCROLL_STEP)
                elif event.button == 5:  # 마우스 휠 아래
                    scroll_offset = min(MAX_SCROLL, scroll_offset + 20)
                    portfolio_scroll_offset = min(PORTFOLIO_MAX_SCROLL, portfolio_scroll_offset + PORTFOLIO_SCROLL_STEP)
                    stock_scroll_offset = min(STOCK_MAX_SCROLL, stock_scroll_offset + STOCK_SCROLL_STEP)
    
                # 매수/매도 버튼 클릭
                if buy_button_rect.collidepoint(event.pos):
                    buy_stock(current_ticker)
                elif sell_button_rect.collidepoint(event.pos):
                    sell_stock(current_ticker)
    
                # 왼쪽 종목 리스트 클릭
                for i, (ticker, rect, rank, price) in enumerate(stock_buttons):
                    shifted_rect = pygame.Rect(rect.x, rect.y - scroll_offset, rect.width, rect.height)
                    if shifted_rect.collidepoint(event.pos):
                        current_ticker_index = i
                        current_ticker = ticker
                        break
                    
                # 아래쪽 종목 그리드 클릭
                for i, (ticker, rect) in enumerate(all_company_buttons):
                    if rect.collidepoint(event.pos):
                        current_ticker = ticker
                        found = False
                        for j, (tk, _, _, _) in enumerate(stock_buttons):
                            if tk == ticker:
                                current_ticker_index = j
                                found = True
                                break
                        if not found:
                            current_ticker_index = 0
                        break
                if back_to_menu_rect.collidepoint(event.pos):
                    game_state = "menu"
                    continue




    # stock_buttons 갱신
        stock_buttons.clear()
        current_prices = []
        for ticker in visible_companies:
            index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
            current_price = prices_by_ticker[ticker][index]
            current_prices.append((ticker, current_price))

        current_prices.sort(key=lambda x: x[1], reverse=True)
        top_10 = current_prices[:10]

        for rank, (ticker, price) in enumerate(top_10, start=1):
            rect = pygame.Rect(
                LAYOUT["stock_list"]["x"],
                LAYOUT["stock_list"]["y_start"] + (len(stock_buttons) * button_height),
                250,
                button_height
            )
            stock_buttons.append((ticker, rect, rank, price))

        # all_company_buttons 갱신
        all_company_buttons.clear()
        total_cells = LAYOUT["grid"]["cols"] * LAYOUT["grid"]["rows"]
        grid_height = LAYOUT["grid"]["cell_height"] * LAYOUT["grid"]["rows"]

        for idx in range(total_cells):
            col = idx % LAYOUT["grid"]["cols"]
            row = idx // LAYOUT["grid"]["cols"]
            x = LAYOUT["grid"]["x"] + col * LAYOUT["grid"]["cell_width"]
            y = LAYOUT["screen"]["height"] - grid_height - LAYOUT["grid"]["y_offset_from_bottom"] + row * LAYOUT["grid"]["cell_height"]

            if idx < len(visible_companies):
                ticker = visible_companies[idx]
                rect = pygame.Rect(x, y, LAYOUT["grid"]["cell_width"], LAYOUT["grid"]["cell_height"])
                all_company_buttons.append((ticker, rect))

        # 그래프와 순위 업데이트
        rank_today = {ticker: rank for rank, (ticker, _) in enumerate(current_prices, start=1)}
        for ticker in rank_today:
            if ticker not in rank_history:
                rank_history[ticker] = {}
            rank_history[ticker][today] = rank_today[ticker]

        # 각 티커 시간 인덱스 진행
        # ✅ 시뮬레이션 하루씩 진행
    if current_day_index + 1 < len(simulation_date_list):
        current_day_index += 1
        today = simulation_date_list[current_day_index]
    
        # 각 티커 인덱스도 날짜에 맞게 조정
        for ticker in TICKERS:
            # 현재 날짜보다 작거나 같은 인덱스를 찾기
            for i, d in enumerate(dates_by_ticker[ticker]):
                d_obj = datetime.datetime.strptime(d, "%y.%m.%d").date()
                if d_obj > today:
                    break
                time_indices[ticker] = i




    # ----- 게임 화면 그리기 -----

    # 🟢 현재 선택된 티커 기준으로 prices, dates 준비
    # 항상 current_ticker를 먼저 안전하게 정의
    # current_ticker_index는 이제 무시하고,
    # current_ticker 값만을 기반으로 처리
    if current_ticker not in prices_by_ticker:
        continue  # 안전하게 체크

    current_index = min(time_indices[current_ticker], len(prices_by_ticker[current_ticker]) - 1)    
    prices = prices_by_ticker[current_ticker][:max(2, current_index + 1)]
    dates = dates_by_ticker[current_ticker][:max(2, current_index + 1)]


    # 🟢 해당 종목이 아직 상장 전이면 스킵
    if simulation_date_list[current_day_index] < first_available_date[current_ticker]:
        pygame.display.flip()
        clock.tick(5)
        if current_day_index + 1 < len(simulation_date_list):
            current_day_index += 1
        continue

    # ----- 게임 화면 그리기 -----
    if chart_zoom_mode:
        draw_zoomed_chart(prices, dates)
    elif input_mode == "save":
        draw_input_box()
    elif input_mode == "load":
        screen.fill((30, 30, 30))
        draw_load_file_buttons()
    else:
        screen.fill((30, 30, 30))
        if game_state == "menu":
            draw_main_menu()
        else:
            draw_ui()


    pygame.display.flip()
    clock.tick(30)  # 초당 프레임 제한 (너무 빠르게 돌지 않도록)
