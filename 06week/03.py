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

for ticker in TICKERS:
    stock_data = yf.download(ticker, period="5d", interval="1h")['Close'].dropna()
    prices_by_ticker[ticker] = list(stock_data.values)

# ----- 2. 게임 상태 초기화 -----
portfolio = {
    'cash': 100000,
    'stocks': {ticker: {'quantity': 0, 'buy_price': 0} for ticker in TICKERS}
}
alerts = []

# ----- 3. Pygame 초기화 및 화면 설정 -----
pygame.init()
WIDTH, HEIGHT = 1000, 700
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
    # Buy 버튼
    pygame.draw.rect(screen, (70, 130, 180), buy_button_rect)  # 파란색 버튼
    buy_text = font.render("Buy", True, (255, 255, 255))
    screen.blit(buy_text, (buy_button_rect.x + 50, buy_button_rect.y + 15))
    
    # Sell 버튼
    pygame.draw.rect(screen, (180, 70, 70), sell_button_rect)  # 빨간색 버튼
    sell_text = font.render("Sell", True, (255, 255, 255))
    screen.blit(sell_text, (sell_button_rect.x + 50, sell_button_rect.y + 15))

def draw_stock_list():
    for i, (ticker, name) in enumerate(TICKERS.items()):
        button = stock_buttons[i]
        pygame.draw.rect(screen, (100, 100, 100), button)  # 회색 버튼
        text = font.render(f"{name} ({ticker})", True, (255, 255, 255))
        screen.blit(text, (button.x + 10, button.y + 10))

def draw_text(text, x, y, color=(255, 255, 255)):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

def draw_chart(prices, offset_x, offset_y, width, height):
    if len(prices) < 2:
        return
    
    max_price = max(prices)
    min_price = min(prices)
    scale = height / (max_price - min_price) if max_price != min_price else 1
    
    for i in range(1, len(prices)):
        x1 = offset_x + (i - 1) * 5
        x2 = offset_x + i * 5
        y1 = offset_y + height - (prices[i - 1] - min_price) * scale
        y2 = offset_y + height - (prices[i] - min_price) * scale
        pygame.draw.line(screen, (0, 255, 0), (x1, int(y1)), (x2, int(y2)), 2)

def show_portfolio():
    draw_text(f"Cash: ${float(portfolio['cash']):.2f}", 10, 10)
    y = 40
    for ticker, info in portfolio['stocks'].items():
        quantity = info['quantity']
        if quantity > 0 and time_index < len(prices_by_ticker[ticker]):
            avg_price = float(info['buy_price'])
            current_price = float(prices_by_ticker[ticker][time_index])
            profit = (current_price - avg_price) * quantity
            color = (255, 0, 0) if profit >= 0 else (0, 128, 255)
            draw_text(f"{ticker}: {quantity} @ ${avg_price:.2f} -> ${current_price:.2f} | Profit: ${profit:.2f}", 10, y, color)
            y += 30

def buy_stock(ticker):
    global alerts
    price = float(prices_by_ticker[ticker][time_index])
    if portfolio['cash'] >= price:
        portfolio['cash'] -= price
        info = portfolio['stocks'][ticker]
        total_cost = info['quantity'] * info['buy_price'] + price
        info['quantity'] += 1
        info['buy_price'] = total_cost / info['quantity']
        alerts.append(f"Bought 1 {ticker}")
    else:
        alerts.append(f"Not enough cash to buy {ticker}")

def sell_stock(ticker):
    global alerts
    info = portfolio['stocks'][ticker]
    if info['quantity'] > 0:
        price = float(prices_by_ticker[ticker][time_index])
        portfolio['cash'] += price
        info['quantity'] -= 1
        alerts.append(f"Sold 1 {ticker}")
        if info['quantity'] == 0:
            info['buy_price'] = 0
    else:
        alerts.append(f"No {ticker} to sell")

def show_alerts():
    for i, msg in enumerate(alerts[-3:]):
        draw_text(msg, WIDTH - 300, HEIGHT - 80 + i * 20, (255, 255, 0))

# ----- 5. 게임 루프 -----
running = True
while running:
    screen.fill((30, 30, 30))  # 배경색 어두운 회색으로 채움
    
    draw_stock_list()  # 주식 목록 그리기
    draw_buttons()  # 매수/매도 버튼 그리기

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                mouse_pos = event.pos
                for i, button in enumerate(stock_buttons):
                    if button.collidepoint(mouse_pos):
                        current_ticker_index = i
                if buy_button_rect.collidepoint(mouse_pos):
                    buy_stock(list(TICKERS.keys())[current_ticker_index])
                elif sell_button_rect.collidepoint(mouse_pos):
                    sell_stock(list(TICKERS.keys())[current_ticker_index])

    current_ticker = list(TICKERS.keys())[current_ticker_index]
    company_name = TICKERS[current_ticker]
    draw_text(f"Selected: {company_name} ({current_ticker})", WIDTH // 2 - 150, 10, (255, 255, 255))
    
    current_prices = prices_by_ticker[current_ticker][:time_index + 1]
    draw_chart(current_prices, 250, 100, 700, 300)

    show_portfolio()
    show_alerts()

    time_index += 1
    if time_index >= len(prices_by_ticker[current_ticker]):
        alerts.append("Simulation ended")
        running = False

    pygame.display.flip()
    clock.tick(1)

pygame.quit()
sys.exit()