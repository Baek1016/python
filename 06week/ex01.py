import pygame

# pygame.init()

# win = pygame.display.set_mode((500, 500))
# pygame.display.set_caption("My Game")

# run = True
# x = 50
# while run:
#     pygame.time.delay(100)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#     win.fill((0, 0, 0))
#     pygame.draw.rect(win, (255, 0, 0), (x, 50, 50, 50))
#     x += 5
#     pygame.display.update()

# pygame.quit()

import yfinance as yf

# 삼성전자 (005930.KQ는 안되고 외국용 티커만 가능, 예시는 애플)
data = yf.download("AAPL", start="2025-03-23", end="2025-03-30", interval="1d")
print(data.head())
