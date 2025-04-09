import yfinance as yf
import pygame
import sys
from datetime import datetime, timedelta

# 1. 데이터 다운로드
ticker = "AAPL"  # 주식 티커
end_date = datetime.today().strftime('%Y-%m-%d')  # 오늘 날짜
start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')  # 7일 전 날짜

# 데이터 다운로드
print(f"Downloading data for {ticker} from {start_date} to {end_date}...")
data = yf.download(ticker, start=start_date, end=end_date, interval="1d")

# 데이터 확인
if data.empty:
    print("❗ 데이터가 비어 있습니다. 날짜 범위나 티커를 확인하세요.")
    sys.exit()

# 'Close' 또는 'Adj Close' 컬럼 확인 및 처리
# 'Close' 또는 'Adj Close' 컬럼 확인 및 처리
if 'Close' in data.columns:
    close_prices = data['Close'].values.flatten().tolist()
elif 'Adj Close' in data.columns:
    print("⚠️ 'Close' 컬럼이 없어 'Adj Close' 컬럼을 대신 사용합니다.")
    close_prices = data['Adj Close'].values.flatten().tolist()
else:
    print("❗ 'Close'와 'Adj Close' 컬럼이 모두 없습니다. 데이터를 확인하세요.")
    print("데이터프레임 내용:")
    print(data.head())
    sys.exit()

# 날짜 데이터 처리
dates = data.index.strftime('%m-%d').tolist()

if not close_prices or not dates:
    print("❗ 그래프를 그릴 데이터가 없습니다.")
    sys.exit()

# 2. 데이터 범위 계산
max_price = max(close_prices)
min_price = min(close_prices)
width, height = 800, 600
bar_width = width // len(close_prices)

# 3. pygame 초기화
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"{ticker} 주식 차트")

font = pygame.font.SysFont("Arial", 16)
clock = pygame.time.Clock()

# 4. 메인 루프
running = True
while running:
    screen.fill((255, 255, 255))  # 배경 흰색

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 주식 막대 그래프 그리기
    for i, price in enumerate(close_prices):
        # 가격을 비율로 높이 계산
        if max_price == min_price:
            bar_height = 0
        else:
            bar_height = int((price - min_price) / (max_price - min_price) * (height - 100))
        x = i * bar_width + 40
        y = height - bar_height - 40
        pygame.draw.rect(screen, (100, 150, 250), (x, y, bar_width - 10, bar_height))

        # 날짜 라벨
        date_text = font.render(dates[i], True, (0, 0, 0))
        screen.blit(date_text, (x, height - 30))

        # 가격 표시
        price_text = font.render(f"{price:.2f}", True, (0, 0, 0))
        screen.blit(price_text, (x, y - 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()