# utils.py

import pygame
from font_loader import font

# ✅ 텍스트를 화면에 출력
def draw_text(text, x, y, color=(255, 255, 255), screen=None):
    if screen is None:
        screen = pygame.display.get_surface()
    if isinstance(color, tuple) and len(color) == 3:
        render = font.render(text, True, color)
        screen.blit(render, (x, y))


# ✅ 알림 저장소
alerts = []
