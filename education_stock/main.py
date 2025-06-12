import pygame
import sys
from game_state import init_game, main_loop, game_mode
from constants import LAYOUT

if __name__ == "__main__":
    pygame.init()
    print("📦 Pygame initialized")

    screen = pygame.display.set_mode(
        (LAYOUT["screen"]["width"], LAYOUT["screen"]["height"])
    )
    pygame.display.set_caption("Stock Simulator")

    try:
        if game_mode == "menu":
            print("✅ 메뉴 화면으로 진입")
        init_game()
    except SystemExit:
        sys.exit()
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")
        sys.exit(1)

    try:
        main_loop(screen)
    except Exception as e:
        print(f"❌ 메인 루프 실행 중 오류 발생: {e}")
        pygame.quit()
        sys.exit(1)

    pygame.quit()
