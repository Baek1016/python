import pygame
import sys
from game_state import init_game, main_loop
from constants import LAYOUT

if __name__ == "__main__":
    pygame.init()
    print("📦 Pygame initialized")

    # ✅ 화면 크기 설정
    screen = pygame.display.set_mode((LAYOUT["screen"]["width"], LAYOUT["screen"]["height"]))
    pygame.display.set_caption("Stock Simulator")

    try:
        init_game()
    except SystemExit:
        sys.exit()
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")
        sys.exit(1)

    # ✅ 메인 루프 실행 (화면 넘김)
    main_loop(screen)

    pygame.quit()
