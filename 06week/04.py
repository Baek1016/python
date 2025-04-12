import yfinance as yf
import pygame
import sys

# ----- 1. 데이터 준비: 여러 종목 데이터 다운로드 -----
TICKERS = {
    'AAPL': 'Apple',
    'GOOG': 'Google',
    'TSLA': 'Tesla'
}
prices_by_ticker = {}
dates_by_ticker = {}

for ticker in TICKERS:
    stock_data = yf.download(ticker, period="5d", interval="1h").dropna()
    prices_by_ticker[ticker] = list(stock_data['Close'].values)
    dates_by_ticker[ticker] = list(stock_data.index.strftime('%m-%d %H:%M'))

# ----- 2. 게임 상태 초기화 -----
portfolio = {
    'cash': 100000,
    'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
}
alerts = []

# ----- 3. Pygame 초기화 및 화면 설정 -----
pygame.init()
WIDTH, HEIGHT = 1200, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stock Trading Simulator")
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

current_ticker_index = 0
time_index = 0

# 버튼 영역 정의
buy_button_rect = pygame.Rect(50, 600, 150, 50)
sell_button_rect = pygame.Rect(250, 600, 150, 50)

# 주식 목록 버튼 정의
stock_buttons = []
for i, ticker in enumerate(TICKERS):
    stock_buttons.append(pygame.Rect(50, 100 + i * 50, 150, 40))

# ----- 4. 함수 정의 -----
def draw_buttons():
    pygame.draw.rect(screen, (70, 130, 180), buy_button_rect)  # 파란색 버튼
    buy_text = font.render("Buy", True, (255, 255, 255))
    screen.blit(buy_text, (buy_button_rect.x + 50, buy_button_rect.y + 15))
    
    pygame.draw.rect(screen, (180, 70, 70), sell_button_rect)  # 빨간색 버튼
    sell_text = font.render("Sell", True, (255, 255, 255))
    screen.blit(sell_text, (sell_button_rect.x + 50, sell_button_rect.y + 15))

def draw_text(text, x, y, color=(255, 255, 255)):
    if x is not None and y is not None and x >= 0 and y >= 0:
        render = font.render(text, True, color)
        screen.blit(render, (x, y))

def draw_chart(prices, dates, offset_x, offset_y, width, height):
    if len(prices) < 2:
        return  # 데이터가 부족하면 차트를 그리지 않음
    
    max_price = float(max(prices))
    min_price = float(min(prices))
    scale = height / (max_price - min_price) if max_price != min_price else 1
    
    # 차트 라인 그리기
    for i in range(1, len(prices)):
        y1_val = prices[i - 1].item() if hasattr(prices[i - 1], "item") else float(prices[i - 1])
        y2_val = prices[i].item() if hasattr(prices[i], "item") else float(prices[i])
        
        y1 = offset_y + height - (y1_val - min_price) * scale
        y2 = offset_y + height - (y2_val - min_price) * scale

        x1 = offset_x + int((i - 1) * width / (len(prices) - 1))
        x2 = offset_x + int(i * width / (len(prices) - 1))
        
        if 0 <= x1 <= WIDTH and 0 <= x2 <= WIDTH and 0 <= y1 <= HEIGHT and 0 <= y2 <= HEIGHT:
            pygame.draw.line(screen, (0, 255, 0), (x1, int(y1)), (x2, int(y2)), 2)

    # y축 가격 눈금
    for i in range(5):
        price = min_price + (max_price - min_price) * (i / 4)
        price = price.item() if hasattr(price, "item") else float(price)  # numpy.ndarray를 스칼라 값으로 변환
        y = offset_y + height - (price - min_price) * scale
        if 0 <= y <= HEIGHT:  # y 값이 화면 범위를 벗어나지 않도록 확인
            draw_text(f"${price:.2f}", offset_x - 50, y, (255, 255, 255))
    
    # x축 날짜 눈금
    for i in range(0, len(dates), max(1, len(dates) // 5)):
        x = offset_x + i * (width // len(prices))
        if 0 <= x <= WIDTH:  # x 값이 화면 범위를 벗어나지 않도록 확인
            draw_text(dates[i], x, offset_y + height + 10, (255, 255, 255))

# ----- 5. 게임 루프 -----
running = True
while running:
    screen.fill((30, 30, 30))  # 배경색 어두운 회색으로 채움
    
    draw_buttons()  # 매수/매도 버튼 그리기

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                mouse_pos = event.pos
                if buy_button_rect.collidepoint(mouse_pos):
                    alerts.append("Buy button clicked!")
                elif sell_button_rect.collidepoint(mouse_pos):
                    alerts.append("Sell button clicked!")

    # 현재 선택된 주식 데이터 가져오기
    current_ticker = list(TICKERS.keys())[current_ticker_index]
    if current_ticker not in prices_by_ticker or len(prices_by_ticker[current_ticker]) == 0:
        draw_text("No data available for the selected stock.", 250, 350, (255, 0, 0))
        pygame.display.flip()
        clock.tick(1)
        continue

    current_prices = prices_by_ticker[current_ticker][:time_index + 1]
    current_dates = dates_by_ticker[current_ticker][:time_index + 1]

    # 차트 그리기
    draw_chart(current_prices, current_dates, 250, 100, 600, 300)

    # time_index 증가 (차트 업데이트)
    time_index += 1
    if time_index >= len(prices_by_ticker[current_ticker]):
        time_index = 0  # 데이터 끝에 도달하면 다시 시작

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
sys.exit()