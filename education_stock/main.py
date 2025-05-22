# main.py

import pygame
import sys
from game_state import init_game, main_loop  # simulation_date_list 제거

if __name__ == "__main__":
    pygame.init()
    print("📦 Pygame initialized")

    try:
        init_game()  # 이 안에서 simulation_date_list 비었는지도 판단함
    except SystemExit:
        sys.exit()
    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}")
        sys.exit(1)

    print("🟢 Starting main loop...")
    main_loop()
