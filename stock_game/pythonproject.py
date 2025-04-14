import yfinance as yf
import pygame
import time
import datetime
import sys
import json
import os
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

SAVE_DIR = "saves"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):

    os.makedirs(CACHE_DIR)

# ----- 1. 데이터 준비: 여러 종목 데이터 다운로드 -----
TICKERS = {
    # 미국
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
    'KO': 'CocaCola',
    'PEP': 'PepsiCo',
    'WMT': 'Walmart',
    'JNJ': 'Johnson & Johnson',
    'V': 'Visa',
    'MA': 'Mastercard',

    # 한국
    '005930.KS': '삼성전자',
    '000660.KS': 'SK하이닉스',
    '066570.KS': 'LG전자',
    '005380.KS': '현대차',
    '035420.KS': 'NAVER',
    '035720.KS': '카카오',

    # 대만
    '2330.TW': 'TSMC',

    # 중국 (홍콩 상장)
    '9988.HK': 'Alibaba',
    '0700.HK': 'Tencent',
    '3690.HK': 'Meituan',
    '1810.HK': 'Xiaomi',

    # 일본
    '6758.T': 'Sony',
    '9984.T': 'SoftBank',
    '7203.T': 'Toyota',

    # 유럽
    'AIR.PA': 'Airbus',
    'OR.PA': 'L’Oreal',
    'NESN.SW': 'Nestlé',
    'SIE.DE': 'Siemens',
    'BMW.DE': 'BMW',
    'SAP.DE': 'SAP',
    'ASML.AS': 'ASML',
    'ULVR.L': 'Unilever',
    'AZN.L': 'AstraZeneca',

    # 남미 (브라질)
    'VALE': 'Vale (Brazil)',
    'PBR': 'Petrobras (Brazil)',
    'ITUB': 'Itaú Unibanco (Brazil)',

    # 캐나다
    'SHOP': 'Shopify',
    'RY': 'Royal Bank of Canada',

    # 인도
    'INFY': 'Infosys',
    'RELIANCE.NS': 'Reliance'
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
        "cols": 5, "rows": 10,
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
menu_new_game_rect = None
menu_continue_rect = None
menu_clear_cache_rect = None


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

volumes_by_ticker = {}
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

# ----- 2. 게임 상태 초기화 -----
simulation_date_list = []
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
# 주식 목록 버튼 정의
stock_buttons = []
for i, ticker in enumerate(TICKERS):
    rect = pygame.Rect(50, 100 + i * button_height, 150, button_height)
    # 기본 rank=0, price=0으로 초기화
    stock_buttons.append((ticker, rect, 0, 0))


# ✅ 스크롤 최대 거리 계산 (아래 공간이 500 픽셀 기준일 때)
MAX_SCROLL = max(0, len(TICKERS) * button_height - 500)


# ----- 4. 함수 정의 -----
def get_stock_data(ticker):
    cache_file = os.path.join(CACHE_DIR, f"{ticker}.csv")
    should_update = True

    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True, encoding="utf-8-sig")
            required_cols = ["open", "high", "low", "close", "volume"]
            missing_cols = [col for col in required_cols if col not in df.columns]

            if df.empty or missing_cols:
                print(f"❌ {ticker} 캐시 오류 → 컬럼 없음 또는 데이터 비어있음 → 삭제함 (없음: {missing_cols})")
                os.remove(cache_file)
                should_update = True
            else:
                should_update = False
                return df
        except Exception as e:
            print(f"⚠ 캐시 파일 읽기 오류: {e}")
            os.remove(cache_file)

    if should_update:
        print(f"📡 캐시 갱신: {ticker}")
        try:
            ticker_obj = yf.Ticker(ticker)
            df = ticker_obj.history(start=start_date, end=end_date, interval="1d", auto_adjust=False)
        except Exception as e:
            print(f"❌ {ticker} 다운로드 실패: {e}")
            return pd.DataFrame()

        # 컬럼 이름을 소문자로 변환
        df.columns = [col.lower() for col in df.columns]

        required_cols = ["open", "high", "low", "close", "volume"]
        if not all(col in df.columns for col in required_cols):
            print(f"❌ {ticker} → 필요한 컬럼 없음 (컬럼들: {df.columns})")
            return pd.DataFrame()

        try:
            df_clean = pd.DataFrame({
                "open": pd.to_numeric(df["open"], errors="coerce"),
                "high": pd.to_numeric(df["high"], errors="coerce"),
                "low": pd.to_numeric(df["low"], errors="coerce"),
                "close": pd.to_numeric(df["close"], errors="coerce"),
                "volume": pd.to_numeric(df["volume"], errors="coerce"),
            }, index=df.index).dropna()

            df_clean.to_csv(cache_file, index=True, encoding="utf-8-sig")
            return df_clean

        except Exception as e:
            print(f"❌ {ticker} 데이터 정리 실패: {e}")
            return pd.DataFrame()


    
from concurrent.futures import ThreadPoolExecutor

def download_one(ticker):
    df = get_stock_data(ticker)
    if df.empty or not all(col in df.columns for col in ["open", "high", "low", "close", "volume"]):
        print(f"❌ {ticker} 데이터에 필요한 컬럼 없음 → 스킵")
        return

    df = df.dropna(subset=["open", "high", "low", "close", "volume"])

    if df.empty or df.isna().sum().sum() > 0:
        print(f"⚠️ {ticker} → NaN 포함 또는 비어 있음 → 스킵")
        return


    try:
        opens = [float(p) for p in df['open']]
        highs = [float(p) for p in df['high']]
        lows = [float(p) for p in df['low']]
        closes = [float(p) for p in df['close']]
        volumes = [int(v) for v in df['volume']]
        dates = [dt.date() if isinstance(dt, pd.Timestamp) else dt for dt in df.index]

        first_date = df.index[0].date()
    except Exception as e:
        print(f"⚠️ {ticker} 변환 실패: {e}")
        return

    # 전역 변수에 저장 (주의: 병렬 환경에서도 안전함)
    prices_by_ticker[f"{ticker}_Open"] = opens
    prices_by_ticker[f"{ticker}_High"] = highs
    prices_by_ticker[f"{ticker}_Low"] = lows
    prices_by_ticker[f"{ticker}_Close"] = closes
    volumes_by_ticker[ticker] = volumes
    dates_by_ticker[ticker] = dates
    first_available_date[ticker] = first_date

def download_all_stock_data():
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_one, TICKERS)

    print("✅ 다운로드 완료된 종목들:", list(prices_by_ticker.keys()))
    print("✅ 정상 처리된 종목 수:", len(prices_by_ticker) // 4)
    if not prices_by_ticker:
        print("❌ 모든 종목 데이터 수집 실패. 캐시를 지우고 다시 시도하세요.")



def init_game():
    global simulation_date_list
    global game_state
    global current_ticker 
    # ✅ 먼저 로딩 메시지를 보여주고
    screen.fill((0, 0, 0))
    loading_font = pygame.font.SysFont(None, 36)
    loading_text = loading_font.render("Downloading stock data...", True, (255, 255, 0))
    screen.blit(loading_text, (LAYOUT["screen"]["width"] // 2 - 150, LAYOUT["screen"]["height"] // 2))
    pygame.display.flip()

    # ✅ 그 다음 데이터를 다운로드함
    download_all_stock_data()
    
    print("📊 다운로드된 티커 확인:")
    for ticker in TICKERS:
        if f"{ticker}_Close" in prices_by_ticker:
            print(f"✅ {ticker} 차트 있음")
        else:
            print(f"❌ {ticker} 차트 없음 (prices_by_ticker에 없음)")


    all_dates = []
    for ticker_dates in dates_by_ticker.values():
        all_dates.extend(ticker_dates)

    if not all_dates:
        print("❗ 데이터가 부족해서 시뮬레이션 날짜 리스트를 만들 수 없습니다.")
        print("📌 캐시 폴더 내용을 지우고 다시 시도해보세요.")
        alerts.append(("❗ 데이터가 부족합니다. 캐시 삭제 후 다시 시도하세요.", time.time()))
        return

    # 여기 추가 로그!
    print("📅 날짜 예시:", all_dates[:5])
    print(f"[디버그] simulation_date_list 길이: {len(simulation_date_list)}")
    print(f"[디버그] prices_by_ticker 키 목록: {list(prices_by_ticker.keys())[:5]}")

    simulation_date_list = sorted(set(all_dates))  # 만약 all_dates가 date 객체면 이대로 OK
    if isinstance(simulation_date_list[0], str):
        simulation_date_list = [datetime.datetime.strptime(d, "%y.%m.%d").date() for d in simulation_date_list]

    simulation_date_list.sort()

    # ✅ 여기서 출력하는 것이 맞음
    print(f"[디버그] 최종 simulation_date_list 길이: {len(simulation_date_list)}")

    print(f"✅ prices_by_ticker 수: {len(prices_by_ticker)}")
    print(f"✅ dates_by_ticker 수: {len(dates_by_ticker)}")
    print(f"✅ simulation_date_list 수: {len(simulation_date_list)}")

    if not simulation_date_list:
        print("❌ 시뮬레이션 날짜 리스트 없음. 게임을 종료합니다.")
        sys.exit()
    # ✅ 마지막에 게임 상태 전환 추가
    game_state = "menu"
    # simulation_date_list가 생성된 후에 이걸로 설정
    if prices_by_ticker:
        for key in prices_by_ticker.keys():
            if key.endswith("_Open"):
                ticker = key.replace("_Open", "")
                # 날짜 타입이 datetime.date인지 확인 후 비교
                if (ticker in first_available_date and 
                    isinstance(first_available_date[ticker], datetime.date) and 
                    first_available_date[ticker] <= simulation_date_list[0]):
                    current_ticker = ticker
                    print(f"✅ 초기 종목 설정: {ticker}, 상장일: {first_available_date[ticker]}")
                    break







def clear_cache():
    deleted = 0
    for fname in os.listdir(CACHE_DIR):
        if fname.endswith(".csv"):
            os.remove(os.path.join(CACHE_DIR, fname))
            deleted += 1
    alerts.append((f"🗑️ 캐시 {deleted}개 삭제됨", time.time()))


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
    print(f"[디버그] draw_chart 호출됨 ✅")
    print(f"  └─ prices 길이: {len(prices)}")
    print(f"  └─ dates 길이: {len(dates)}")

    current_index = min(time_indices[current_ticker], len(prices_by_ticker[f"{current_ticker}_Close"]) - 1)
    
    # 차트 위치와 크기
    chart_layout = LAYOUT["chart"]
    offset_x = chart_layout["x"]
    offset_y = chart_layout["y"]
    width = chart_layout["width"]
    height = chart_layout["height"]

    if len(prices) < 2:
        draw_text("No price variation", offset_x, offset_y + height // 2, (200, 100, 100))
        return

    draw_text(f"Stock Chart: {TICKERS[current_ticker]} ({current_ticker})", offset_x, offset_y - 30, (255, 255, 0))
    
    # 보여줄 범위
    start_index = max(0, current_index - int(width))
    dates_view = dates[start_index:current_index + 1]

    opens = prices_by_ticker[current_ticker + "_Open"][start_index:current_index + 1]
    highs = prices_by_ticker[current_ticker + "_High"][start_index:current_index + 1]
    lows = prices_by_ticker[current_ticker + "_Low"][start_index:current_index + 1]
    closes = prices_by_ticker[current_ticker + "_Close"][start_index:current_index + 1]

    if not (opens and closes and highs and lows):
        return

    # 가격 범위 계산은 딱 1번만!
    max_price = max(highs)
    min_price = min(lows)

    if max_price == min_price:
        draw_text("⚠ 가격 변화 없음", offset_x, offset_y + height // 2, (200, 100, 100))
        return

    scale = height / (max_price - min_price)
    bar_width = width / len(closes)
    # bar_width = min(bar_width, 10)  # ✅ 이 줄 추가

    # 캔들 차트 그리기
    for i in range(len(closes)):
        o = opens[i]
        h = highs[i]
        l = lows[i]
        c = closes[i]

        color = (255, 0, 0) if c > o else (0, 128, 255)

        x = offset_x + i * bar_width
        y_open = offset_y + height - (o - min_price) * scale
        y_close = offset_y + height - (c - min_price) * scale
        y_high = offset_y + height - (h - min_price) * scale
        y_low = offset_y + height - (l - min_price) * scale

        # 십자선 (위꼬리 + 아래꼬리)
        pygame.draw.line(screen, color, (x + bar_width / 2, y_high), (x + bar_width / 2, y_low), 1)

        # 몸통
        top = min(y_open, y_close)
        body_height = max(abs(y_open - y_close), 1)
        pygame.draw.rect(screen, color, (x, top, bar_width * 0.8, body_height))

    # Y축 눈금
    price_range = max_price - min_price
    num_horizontal = min(max(int(price_range // 10), 4), 10)
    price_step = price_range / num_horizontal

    for i in range(num_horizontal + 1):
        y_line = offset_y + i * (height / num_horizontal)
        pygame.draw.line(screen, (80, 80, 80), (offset_x, y_line), (offset_x + width, y_line), 1)
        price_tick = max_price - i * price_step
        draw_text(f"${price_tick:.2f}", offset_x - 60, y_line - 10, (200, 200, 200))

    # X축 눈금
    num_vertical = 6
    for j in range(num_vertical + 1):
        x_line = offset_x + j * (width / num_vertical)
        pygame.draw.line(screen, (80, 80, 80), (x_line, offset_y), (x_line, offset_y + height), 1)
        index = int(j * (len(dates_view) - 1) / num_vertical)
        date_label = dates_view[index]

        # 날짜가 datetime.date나 datetime.datetime이 아니면 파싱 시도
        if isinstance(date_label, datetime.datetime):
            label = date_label.date().strftime("%y.%m.%d")
        elif isinstance(date_label, datetime.date):
            label = date_label.strftime("%y.%m.%d")
        else:
            try:
                parsed_date = datetime.datetime.strptime(str(date_label), "%Y-%m-%d")
                label = parsed_date.strftime("%y.%m.%d")
            except:
                label = str(date_label)[:10]


        draw_text(label, x_line - 25, offset_y + height + 5, (200, 200, 200))


    # 선 그래프 (보조)
    points = []
    if len(closes) < 2:
        return  # 🔐 closes가 너무 짧으면 그래프 생략

    for i, price in enumerate(closes):
        x_point = offset_x + i * (width / (len(closes) - 1))
        y_point = offset_y + height - (price - min_price) * scale
        points.append((float(x_point), float(y_point)))

    if len(points) >= 2:
        pygame.draw.lines(screen, (0, 255, 0), False, points, 2)

    # 거래량
    volume_offset_y = offset_y + height + 20
    volume_height = 50
    volumes = volumes_by_ticker.get(current_ticker, [])
    if len(volumes) < len(closes):
        volumes += [0] * (len(closes) - len(volumes))
    volumes_to_draw = volumes[start_index:current_index + 1]
    draw_volume_bars(volumes_to_draw, offset_x, volume_offset_y, width, volume_height)
    draw_text("Volume", offset_x, volume_offset_y - 20, (100, 200, 255))


def draw_volume_bars(volumes, offset_x, offset_y, width, height):
    if len(volumes) < 2:
        return

    max_volume = max(volumes)
    if max_volume == 0:
        return

    bar_width = width / len(volumes)
    for i, volume in enumerate(volumes):
        x = offset_x + i * bar_width
        bar_height = max(3, (volume / max_volume) * height)
        y = offset_y + height - bar_height
        pygame.draw.rect(screen, (100, 200, 255), (x, y, bar_width * 0.9, bar_height))



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

        index = min(time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
        current_price = float(prices_by_ticker[f"{ticker}_Close"][index])

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
    visible_companies = [
        ticker for ticker in TICKERS
        if ticker in first_available_date and first_available_date[ticker] <= today
    ]


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
        index = min(time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
        current_price = prices_by_ticker[f"{ticker}_Close"][index]

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

def buy_stock(ticker):
    global alerts
    
    index = min(time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    price = float(prices_by_ticker[f"{ticker}_Close"][index])


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
    index = min(time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
    prices = prices_by_ticker[f"{ticker}_Close"][:max(2, index + 1)]

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


def draw_total_profit():
    total_invested = 0.0
    total_current_value = 0.0

    for ticker, data in portfolio["stocks"].items():
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

    draw_text(f"Total Invested: ${total_invested:.2f}", x, y, (255, 255, 255))
    draw_text(f"Current Value: ${total_current_value:.2f}", x, y + 20, (255, 255, 255))
    draw_text(f"Total Profit: ${total_profit:+.2f} ({profit_percent:+.2f}%)", x, y + 40, color)


def get_sorted_visible_stocks():
    today = simulation_date_list[current_day_index]
    visible = []

    for ticker in TICKERS:
        if ticker in first_available_date and first_available_date[ticker] <= today:
            quantity = portfolio["stocks"][ticker]["quantity"]
            price_index = min(time_indices[ticker], len(prices_by_ticker[ticker]) - 1)
            current_price = prices_by_ticker[ticker][price_index]
            total_value = quantity * current_price
            visible.append((ticker, total_value))

    # 가치 기준 정렬 (내림차순)
    visible.sort(key=lambda x: -x[1])
    return visible

def draw_zoomed_chart(opens, highs, lows, closes, dates):
    screen.fill((0, 0, 0))
    offset_x, offset_y = 80, 80
    width = LAYOUT["screen"]["width"] - 160
    height = 400

    total_len = time_indices[current_ticker] + 1
    view_len = int(total_len * chart_zoom_scale)
    total_len = len(closes)
    center_index = time_indices[current_ticker]
    start = max(0, center_index - view_len // 2)
    end = min(total_len, start + view_len)


    opens_view = opens[start:end]
    highs_view = highs[start:end]
    lows_view = lows[start:end]
    closes_view = closes[start:end]
    dates_view = dates[start:end]

    if len(closes_view) < 2:
        return

    max_price = max(highs_view)
    min_price = min(lows_view)

    if max_price == min_price:
        draw_text("⚠ 가격 변화 없음 (확대)", offset_x + 100, offset_y + height // 2, (255, 100, 100))
        return

    scale = height / (max_price - min_price)
    bar_width = width / len(closes_view)

    # 🟥🟦 캔들 차트
    for i in range(len(closes_view)):
        o = opens_view[i]
        h = highs_view[i]
        l = lows_view[i]
        c = closes_view[i]

        color = (255, 0, 0) if c > o else (0, 128, 255)

        x = offset_x + i * bar_width
        y_open = offset_y + height - (o - min_price) * scale
        y_close = offset_y + height - (c - min_price) * scale
        y_high = offset_y + height - (h - min_price) * scale
        y_low = offset_y + height - (l - min_price) * scale

        # 꼬리 선
        pygame.draw.line(screen, color, (x + bar_width / 2, y_high), (x + bar_width / 2, y_low), 1)

        # 몸통
        top = min(y_open, y_close)
        body_height = max(abs(y_open - y_close), 1)
        pygame.draw.rect(screen, color, (x, top, bar_width * 0.8, body_height))

    # 🔡 X축 날짜 라벨
    for i in range(6):
        x_tick = offset_x + i * width / 5
        idx = int(i * (len(dates_view) - 1) / 5)
        pygame.draw.line(screen, (60, 60, 60), (x_tick, offset_y), (x_tick, offset_y + height))
        # 날짜가 datetime.date 타입인지 먼저 확인
        label_date = dates_view[idx]
        if isinstance(label_date, str):
            label = label_date[:7]
        else:
            label = label_date.strftime("%y.%m.%d")[:7]

        draw_text(label, x_tick - 25, offset_y + height + 5, (200, 200, 200))


    # 🔢 Y축 가격 눈금
    for i in range(5):
        y = offset_y + i * height / 4
        val = max_price - i * (max_price - min_price) / 4
        pygame.draw.line(screen, (60, 60, 60), (offset_x, y), (offset_x + width, y))
        draw_text(f"${val:.2f}", offset_x - 60, y - 10, (200, 200, 200))

    draw_text("ESC to exit zoom", offset_x, offset_y + height + 40, (255, 255, 255))

    # 📊 거래량 그리기
    volume_offset_y = offset_y + height + 60
    volume_height = 80
    volumes = volumes_by_ticker.get(current_ticker, [])
    if len(volumes) < end:
        volumes += [0] * (end - len(volumes))  # 부족한 경우 채워줌
    volumes_view = volumes[start:end]  # ✅ 정확한 범위로 슬라이싱


    draw_volume_bars(volumes_view, offset_x, volume_offset_y, width, volume_height)
    draw_text("Volume", offset_x, volume_offset_y - 20, (100, 200, 255))




def draw_ui():
    today = simulation_date_list[current_day_index]
    visible_companies = [
        ticker for ticker in TICKERS
        if ticker in first_available_date and first_available_date[ticker] <= today
    ]

    draw_stock_list(visible_companies)
    cash()
    draw_alerts()
    y_after_profit = draw_portfolio_summary()
    global buy_button_rect, sell_button_rect
    buy_button_rect, sell_button_rect = draw_buttons(y_after_profit)
    draw_all_companies_grid()

    close_key = f"{current_ticker}_Close"
    if close_key in prices_by_ticker:
        current_index = min(time_indices[current_ticker], len(prices_by_ticker[close_key]) - 1)
        prices = prices_by_ticker[close_key][:max(2, current_index + 1)]
        dates = dates_by_ticker[current_ticker][:max(2, current_index + 1)]
        draw_chart(prices, dates)
    
        print(f"📈 current_ticker: {current_ticker}, prices 길이: {len(prices)}, dates 길이: {len(dates)}")

    
    # 🟡 뒤로가기 버튼
    pygame.draw.rect(screen, (150, 150, 150), back_to_menu_rect)
    draw_text("← Menu", back_to_menu_rect.x + 10, back_to_menu_rect.y + 5)

def draw_main_menu():
    global menu_new_game_rect, menu_continue_rect, menu_clear_cache_rect

    screen.fill((20, 20, 20))  # ✅ 먼저 화면을 지워주고 나머지 요소 그리기 시작ㅍㅍ

    title = font.render(" stock simulator", True, (255, 255, 0))
    screen.blit(title, (LAYOUT["screen"]["width"] // 2 - 100, 100))

    menu_new_game_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 100, 200, 200, 50)
    menu_continue_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 100, 270, 200, 50)
    menu_clear_cache_rect = pygame.Rect(LAYOUT["screen"]["width"] // 2 - 100, 340, 200, 50)

    pygame.draw.rect(screen, (70, 130, 180), menu_new_game_rect)
    pygame.draw.rect(screen, (100, 100, 100), menu_continue_rect)
    pygame.draw.rect(screen, (180, 70, 70), menu_clear_cache_rect)

    screen.blit(font.render("new game start", True, (255, 255, 255)), (menu_new_game_rect.x + 30, menu_new_game_rect.y + 15))
    screen.blit(font.render("load game", True, (255, 255, 255)), (menu_continue_rect.x + 50, menu_continue_rect.y + 15))
    screen.blit(font.render("Clear Cache", True, (255, 255, 255)), (menu_clear_cache_rect.x + 40, menu_clear_cache_rect.y + 15))

    if input_mode == "load":
        draw_load_file_buttons()



# ----- 5. 메인 루프 -----
def main_loop():
    if not simulation_date_list:
        print("❌ simulation_date_list가 비어있습니다. 게임을 시작할 수 없습니다.")
        return

    global current_day_index, current_ticker
    global chart_zoom_mode, chart_zoom_scale, chart_zoom_center_ratio
    global input_mode, input_text, load_file_buttons
    global game_state
    last_day_update_time = time.time()


    running = True
    while running:
        screen.fill((30, 30, 30))

        today = simulation_date_list[current_day_index]
        if isinstance(today, str):
            today = datetime.datetime.strptime(today, "%y.%m.%d").date()


        visible_companies = [
            ticker for ticker in TICKERS
            if ticker in first_available_date and first_available_date[ticker] <= today
        ]


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if chart_zoom_mode:
                if event.type == pygame.KEYDOWN:
                    print("📥 키 입력 감지됨 (zoom mode)")
                    if event.key == pygame.K_ESCAPE:
                        print("🔙 ESC 입력 → chart_zoom_mode 종료")
                        chart_zoom_mode = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        chart_zoom_scale = max(0.1, chart_zoom_scale - 0.1)
                    elif event.button == 5:
                        chart_zoom_scale = min(2.0, chart_zoom_scale + 0.1)
                continue

            if input_mode == "save":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        save_game(input_text.strip() + ".json")
                        input_mode = None
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if load_back_button_rect.collidepoint(event.pos):
                        input_mode = None
                        input_text = ""
                continue

            if game_state == "playing" and event.type == pygame.KEYDOWN:
                # 🔹 Shift + S → 다른 이름 저장
                if event.key == pygame.K_s and (event.mod & pygame.KMOD_SHIFT):
                    input_mode = "save"
                    input_text = ""
                    continue
                
                # 🔹 그냥 S → autosave.json 으로 자동 저장
                elif event.key == pygame.K_s:
                    save_game()
                    continue

                # 🔹 L 키 → 저장 파일 불러오기 모드
                if event.key == pygame.K_l:
                    input_mode = "load"
                    continue




            if input_mode == "load":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if load_back_button_rect.collidepoint(event.pos):
                        input_mode = None
                        continue
                    for fname, load_rect, del_rect in load_file_buttons:
                        if load_rect.collidepoint(event.pos):
                            load_game(fname)
                            input_mode = None
                            break
                        elif del_rect.collidepoint(event.pos):
                            os.remove(os.path.join(SAVE_DIR, fname))
                            draw_load_file_buttons()
                            alerts.append((f"{fname} 삭제됨", time.time()))
                            break
                continue

            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if menu_new_game_rect and menu_new_game_rect.collidepoint(event.pos):
                        game_state = "playing"
                        current_day_index = 0
                        portfolio = {
                            'cash': 100000,
                            'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
                        }
                    elif menu_continue_rect and menu_continue_rect.collidepoint(event.pos):
                        input_mode = "load"
                    elif menu_clear_cache_rect and menu_clear_cache_rect.collidepoint(event.pos):
                        clear_cache()
                continue


            if game_state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_to_menu_rect.collidepoint(event.pos):
                        game_state = "menu"
                        continue
                    if buy_button_rect.collidepoint(event.pos):
                        buy_stock(current_ticker)
                        continue
                    if sell_button_rect.collidepoint(event.pos):
                        sell_stock(current_ticker)
                        continue
                    chart_rect = pygame.Rect(LAYOUT["chart"]["x"], LAYOUT["chart"]["y"], LAYOUT["chart"]["width"], LAYOUT["chart"]["height"])
                    if chart_rect.collidepoint(event.pos):
                        chart_zoom_mode = True
                        chart_zoom_center_ratio = (event.pos[0] - chart_rect.x) / chart_rect.width
                        continue
                    for ticker, rect, rank, price in stock_buttons:
                        shifted_rect = pygame.Rect(rect.x, rect.y - stock_scroll_offset, rect.width, rect.height)
                        if shifted_rect.collidepoint(event.pos):
                            current_ticker = ticker
                            break
                    for ticker, rect in all_company_buttons:
                        if rect.collidepoint(event.pos):
                            current_ticker = ticker
                            break

        stock_buttons.clear()
        current_prices = []
        for ticker in visible_companies:
            index = min(time_indices[ticker], len(prices_by_ticker[f"{ticker}_Close"]) - 1)
            current_price = prices_by_ticker[f"{ticker}_Close"][index]

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

        rank_today = {ticker: rank for rank, (ticker, _) in enumerate(current_prices, start=1)}

        for ticker in rank_today:
            if ticker not in rank_history:
                rank_history[ticker] = {}
            rank_history[ticker][today] = rank_today[ticker]


        # 하루가 3분마다 진행되도록 조정
        if time.time() - last_day_update_time > 10:
            if current_day_index + 1 < len(simulation_date_list):
                current_day_index += 1
                last_day_update_time = time.time()
                today = simulation_date_list[current_day_index]
            else:
                alerts.append(("⏱️ 시뮬레이션 종료 - 더 이상 진행할 날짜가 없습니다.", time.time()))

        # ✅ 날짜 진행 후, 각 ticker의 time_indices를 갱신
        for ticker in TICKERS:
            if ticker not in dates_by_ticker:
                continue
            
            for i, d in enumerate(dates_by_ticker[ticker]):
                d_obj = d if isinstance(d, datetime.date) else datetime.datetime.strptime(d, "%y.%m.%d").date()

                if d_obj > today:
                    break
                time_indices[ticker] = i

            # 필요 시 아래처럼 menu로 돌아가거나, 멈춤 처리도 가능
            # game_state = "menu"
            # running = False


            # ✅ 문자열이면 날짜로 바꿔줘야 함!
            if isinstance(today, str):
                today = datetime.datetime.strptime(today, "%y.%m.%d").date()
                simulation_date_list[current_day_index] = today

            for ticker in TICKERS:
                if ticker not in dates_by_ticker:
                    continue
                
                for i, d in enumerate(dates_by_ticker[ticker]):
                    d_obj = d if isinstance(d, datetime.date) else datetime.datetime.strptime(d, "%y.%m.%d").date()
                    if d_obj > today:
                        break
                    time_indices[ticker] = i

        # ----- 게임 화면 그리기 -----

        # 🟢 현재 선택된 티커 기준으로 prices, dates 준비
        # 항상 current_ticker를 먼저 안전하게 정의
        # current_ticker_index는 이제 무시하고,
        # current_ticker 값만을 기반으로 처리
        if current_ticker not in prices_by_ticker:
            prices = []
            dates = []
        else:
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
        screen.fill((30, 30, 30))

        if chart_zoom_mode:
            draw_zoomed_chart(
                prices_by_ticker[f"{current_ticker}_Open"],
                prices_by_ticker[f"{current_ticker}_High"],
                prices_by_ticker[f"{current_ticker}_Low"],
                prices_by_ticker[f"{current_ticker}_Close"],
                dates_by_ticker[current_ticker]
            )
        elif input_mode == "save":
            draw_input_box()
        elif input_mode == "load":
            draw_load_file_buttons()
        elif game_state == "menu":
            draw_main_menu()
        else:
            draw_ui()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    init_game()

    print(f"🎯 최종 날짜 리스트 길이 확인: {len(simulation_date_list)}")  # <-- 디버깅용

    if not simulation_date_list:
        print("❌ 날짜 리스트 없음 → 게임 시작 불가. 캐시를 삭제하거나 인터넷 연결을 확인하세요.")
        sys.exit()

    print("🟢 main_loop 시작")  # <- 여기도 디버깅 추가
    main_loop()


