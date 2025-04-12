import yfinance as yf
import pygame
import time
import datetime
import sys

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

# ✅ UI 레이아웃을 하나의 딕셔너리로 통합 관리하도록 구조화
LAYOUT = {
    "screen": {"width": 1000, "height": 700},
    "chart": {"x": 450, "y": 60, "width": 650, "height": 300},
    "buttons": {
        "buy": {"width": 150, "height": 50, "offset_x": 0},
        "sell": {"width": 150, "height": 50, "offset_x": 200},
        "offset_y": 20  # 차트 아래 간격
    },
    "stock_list": {
        "x": 50, "y_start": 100, "button_height": 40, "visible_height": 400
    },
    "grid": {
        "x": 50, "y_offset_from_bottom": 10, "cols": 4, "cell_width": 150, "cell_height": 40, "rows": 5
    },
    "portfolio": {
        "x": 1150, "y_start": 100, "visible_height": 500, "line_height": 30
    },
    "alerts": {"x": 700, "y_base": 620, "line_height": 20, "max": 3},
    "profit_summary": {"x": 980, "y": 10}
}

all_company_buttons = []
portfolio_scroll_offset = 0
PORTFOLIO_SCROLL_STEP = 20
PORTFOLIO_MAX_SCROLL = 0

stock_scroll_offset = 0
STOCK_SCROLL_STEP = 20
STOCK_MAX_SCROLL = 0
CHART_X = 450

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
portfolio = {
    'cash': 100000,
    'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
}
alerts = []

# ----- 3. Pygame 초기화 및 화면 설정 -----
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Stock Trading Simulator")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

current_ticker_index = 0
time_indices = {ticker: 0 for ticker in TICKERS}

chart_y = 100
chart_height = 300
button_y = chart_y + chart_height + 20  # 차트 아래 20 픽셀 간격

buy_button_rect = pygame.Rect(CHART_X, button_y, 150, 50)
sell_button_rect = pygame.Rect(CHART_X + 200, button_y, 150, 50)


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
def draw_buttons():
    # Buy 버튼
    pygame.draw.rect(screen, (70, 130, 180), buy_button_rect)  # 파란색 버튼
    buy_text = font.render("Buy", True, (255, 255, 255))
    screen.blit(buy_text, (buy_button_rect.x + 50, buy_button_rect.y + 15))
    
    # Sell 버튼
    pygame.draw.rect(screen, (180, 70, 70), sell_button_rect)  # 빨간색 버튼
    sell_text = font.render("Sell", True, (255, 255, 255))
    screen.blit(sell_text, (sell_button_rect.x + 50, sell_button_rect.y + 15))

def cash():
    draw_text(f"Cash: ${float(portfolio['cash']):.2f}", 10, 10)

def draw_all_companies_grid():
    today = simulation_date_list[current_day_index]
    visible_companies = [ticker for ticker in TICKERS if first_available_date[ticker] <= today]
    
    grid_x = 50
    grid_y = HEIGHT - 5 * 40 - 10  # 🔧 화면 아래에서 5줄 공간 확보
    cell_width, cell_height = 150, 40
    cols = 4
    total_cells = 20  # 4x5 고정

    for idx in range(total_cells):
        col = idx % cols
        row = idx // cols
        x = grid_x + col * cell_width
        y = grid_y + row * cell_height

        if idx < len(visible_companies):
            ticker = visible_companies[idx]
            rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2)
            draw_text(f"{TICKERS[ticker]} ({ticker})", x + 5, y + 10)
            all_company_buttons.append((ticker, rect))
        else:
            rect = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, (50, 50, 50), rect, 2)



def draw_stock_list():
    draw_text("📈 Current Stock Rankings", 50, 60, (255, 255, 0))  # 제목
    today = simulation_date_list[current_day_index]
    
    current_prices = []
    for ticker in TICKERS:
        if first_available_date[ticker] <= today:
            index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
            current_price = prices_by_ticker[ticker][index]
            current_prices.append((ticker, current_price))
    
    current_prices.sort(key=lambda x: x[1], reverse=True)

    stock_buttons.clear()
    top_10 = current_prices[:10]  # ✅ 10개만 잘라서 보여줌

    for rank, (ticker, price) in enumerate(top_10, start=1):
        rect = pygame.Rect(50, 100 + len(stock_buttons) * button_height, 250, button_height)
        stock_buttons.append((ticker, rect, rank, price))

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
    STOCK_MAX_SCROLL = max(0, len(top_10) * button_height - 400)  # 400은 표시 영역 높이


def draw_text(text, x, y, color=(255, 255, 255)):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

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

def show_alerts():
    now = time.time()
    duration = 1.5  # 초단위, 몇 초 동안 보여줄지

    # 오래된 메시지 제거
    alerts[:] = [entry for entry in alerts if now - entry[1] <= duration]

    # 최근 메시지 3개만 보여줌
    for i, (msg, _) in enumerate(alerts[-3:]):
        draw_text(msg, WIDTH - 300, HEIGHT - 80 + i * 20, (255, 255, 0))

def draw_chart(prices, dates, offset_x, offset_y, width, height):
    if len(prices) < 2:
        return

    draw_text(f"Stock Chart: {TICKERS[current_ticker]} ({current_ticker})", offset_x, offset_y - 30, (255, 255, 0))
    
    prices = [float(p) for p in prices]
    max_price = max(prices)
    min_price = min(prices)
    scale = height / (max_price - min_price) if max_price != min_price else 1

    # --- 1. Y축 (가격) 눈금 자동 계산 ---
    price_range = max_price - min_price
    # 가격 차이에 따라 눈금 개수 조절 (최소 4, 최대 10)
    num_horizontal = min(max(int(price_range // 10), 4), 10)
    price_step = price_range / num_horizontal

    for i in range(num_horizontal + 1):
        y_line = offset_y + i * (height / num_horizontal)
        pygame.draw.line(screen, (80, 80, 80), (offset_x, y_line), (offset_x + width, y_line), 1)
        price_tick = max_price - i * price_step
        draw_text(f"${price_tick:.2f}", offset_x - 60, y_line - 10, (200, 200, 200))

    # --- 2. X축 (날짜) 눈금 ---
    num_vertical = 6  # x축 눈금 개수 (너무 많으면 겹침)
    for j in range(num_vertical + 1):
        x_line = offset_x + j * (width / num_vertical)
        pygame.draw.line(screen, (80, 80, 80), (x_line, offset_y), (x_line, offset_y + height), 1)
        index = int(j * (len(dates) - 1) / num_vertical)
        # 날짜 형식: 예 "2021-08" 또는 "2021-08-15"
        date_label = dates[index]
        # 연도-월 또는 연도-월-일 형식 유지
        draw_text(date_label[:7], x_line - 25, offset_y + height + 5, (200, 200, 200))

    # --- 3. 주가 선 그래프 그리기 ---
    points = []
    for i, price in enumerate(prices):
        x_point = offset_x + i * (width / (len(prices) - 1))
        y_point = offset_y + height - (price - min_price) * scale
        points.append((float(x_point), float(y_point)))

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)

def draw_rank_chart(rank_history, offset_x, offset_y, width, height):
    if not rank_history:
        return

    tickers = list(rank_history.keys())
    date_list = list(rank_history[tickers[0]].keys())
    num_dates = len(date_list)

    if num_dates <= 1:
        return  # 🚨 날짜가 1개 이하일 땐 그래프 그리지 않음
    
    max_rank = max(len(tickers), 10)
    scale_x = width / (num_dates - 1)
    scale_y = height / max_rank

    # 선 그리기
    for ticker in tickers:
        points = []
        for i, date in enumerate(date_list):
            rank = rank_history[ticker].get(date, None)
            if rank is None: continue
            x = offset_x + i * scale_x
            y = offset_y + (rank - 1) * scale_y  # 1등은 위
            points.append((x, y))
        if len(points) >= 2:
            pygame.draw.lines(screen, (0, 255, 255), False, points, 2)

    # Y축 눈금 라벨 표시 (선택 사항)
    for r in range(1, max_rank + 1):
        y_line = offset_y + (r - 1) * scale_y
        draw_text(f"{r}위", offset_x - 30, y_line - 10, (200, 200, 200))


def draw_portfolio_summary():
    x = CHART_X + 700
    y_start = 100
    y = y_start - portfolio_scroll_offset
    line_height = 30
    total_items = 0  # 표시된 항목 수

    draw_text("📊 Portfolio", x, y - 40, ( 255, 255, 0))

    total_invested = 0.0
    total_current_value = 0.0

    for ticker, data in portfolio["stocks"].items():
        quantity = data["quantity"]
        if quantity == 0:
            continue

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

        # 종합 수익 계산
        total_invested += quantity * avg_price
        total_current_value += quantity * current_price

    # 총 수익 계산 후 맨 아래에 표시
    if total_invested > 0:
        total_profit = total_current_value - total_invested
        profit_percent = (total_profit / total_invested) * 100
    else:
        total_profit = 0
        profit_percent = 0

    color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)

    y += 20  # 약간의 간격
    draw_text(f"Total Invested: ${total_invested:.2f}", x, y, (255, 255, 255))
    draw_text(f"Current Value: ${total_current_value:.2f}", x, y + 20, (255, 255, 255))
    draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y + 40, color)

    # 스크롤 최대값 설정 (총 높이 계산)
    total_height = (total_items * (line_height + 10)) + 100  # 종합 수익까지 포함
    global PORTFOLIO_MAX_SCROLL
    PORTFOLIO_MAX_SCROLL = max(0, total_height - 500)  # 500은 표시 가능한 높이 기준



def draw_total_profit():
    total_invested = 0.0
    total_current_value = 0.0
    # portfolio 내 주식 정보는 portfolio["stocks"] 에 저장되어 있습니다.
    for ticker, data in portfolio["stocks"].items():
        quantity = data["quantity"]
        if quantity > 0:
            invested = quantity * data["buy_price"]  # 투자 당시 총액
            current_price = float(prices_by_ticker[ticker][time_indices[ticker]])
            current_value = quantity * current_price
            total_invested += invested
            total_current_value += current_value

    # 총 수익과 수익률 계산
    if total_invested > 0:
        total_profit = total_current_value - total_invested
        profit_percent = (total_profit / total_invested) * 100
    else:
        total_profit = 0
        profit_percent = 0

    # 수익률에 따른 색상 설정: 이익이면 빨간색, 손해이면 파란색
    color = (255, 0, 0) if profit_percent >= 0 else (0, 128, 255)
    
    # 예시: 전체 투자 정보를 화면 오른쪽 상단(또는 원하는 위치)에 표시
    x = 980  # x 좌표 (화면 오른쪽에 배치)
    y = 10   # y 좌표 (원하는 위치로 조정)
    
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


# ----- 5. 메인 루프 -----
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_offset = max(0, scroll_offset - 20)
                portfolio_scroll_offset = max(0, portfolio_scroll_offset - PORTFOLIO_SCROLL_STEP)
                stock_scroll_offset = max(0, stock_scroll_offset - STOCK_SCROLL_STEP)
            elif event.button == 5:  # Scroll down
                scroll_offset = min(MAX_SCROLL, scroll_offset + 20)
                portfolio_scroll_offset = min(PORTFOLIO_MAX_SCROLL, portfolio_scroll_offset + PORTFOLIO_SCROLL_STEP)
                stock_scroll_offset = min(STOCK_MAX_SCROLL, stock_scroll_offset + STOCK_SCROLL_STEP)
            # 회사 전체 목록 클릭 처리
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
                        # 만약 top10에 없던 티커라면 기본 인덱스로 설정
                        current_ticker_index = 0
                    break
            # 🖱 버튼 클릭 처리
            if buy_button_rect.collidepoint(event.pos):
                buy_stock(current_ticker)  # ✅ 현재 선택된 티커로 매수
            elif sell_button_rect.collidepoint(event.pos):
                sell_stock(current_ticker)  # ✅ 현재 선택된 티커로 매도
            # 🖱 스크롤된 위치 반영해서 버튼 클릭 처리
            for i, (ticker, rect, rank, price) in enumerate(stock_buttons):
                shifted_rect = pygame.Rect(rect.x, rect.y - scroll_offset, rect.width, rect.height)
                if shifted_rect.collidepoint(event.pos):
                    current_ticker_index = i
                    current_ticker = ticker  # ✅ 현재 티커를 직접 저장
                    break
    # ----- 게임 화면 그리기 -----
    draw_stock_list()
    cash()
    show_alerts()
    draw_portfolio_summary()
    draw_buttons()
    all_company_buttons.clear()
    draw_all_companies_grid()

    

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

    # ✅ 주가 차트 먼저
    draw_chart(prices, dates, CHART_X, chart_y, 650, chart_height)

    # ✅ 순위 기록 저장 (매 프레임)
    today = simulation_date_list[current_day_index]
    current_prices = []
    for ticker in TICKERS:
        if first_available_date[ticker] <= today:
            index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
            current_price = prices_by_ticker[ticker][index]
            current_prices.append((ticker, current_price))

    current_prices.sort(key=lambda x: x[1], reverse=True)
    rank_today = {ticker: rank for rank, (ticker, _) in enumerate(current_prices, start=1)}
    for ticker in rank_today:
        if today not in rank_history[ticker]:
            rank_history[ticker][today] = rank_today[ticker]

    # ✅ 순위 그래프 차트 그리기 (주가 차트 아래에)
    draw_rank_chart(rank_history, offset_x=250, offset_y=button_y + 100, width=700, height=180)

    pygame.display.flip()
    clock.tick(5)

    # ⏩ 시간 진행
    for ticker in TICKERS:
        if time_indices[ticker] + 1 < len(prices_by_ticker[ticker]):
            time_indices[ticker] += 1

