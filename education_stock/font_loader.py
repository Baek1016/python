# font_loader.py
import pygame

# 폰트 경로 및 사이즈를 필요에 따라 조절
pygame.font.init()
font = pygame.font.SysFont("Arial", 18)
title_font = pygame.font.SysFont("Arial", 22, bold=True)
large_font = pygame.font.SysFont("Arial", 28, bold=True)

__all__ = ["font", "title_font", "large_font"]
