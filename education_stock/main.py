import pygame
import sys
import time
from game_state import init_game, main_loop, game_mode, selected_save_file
from constants import LAYOUT
from ui_drawer import draw_main_menu, draw_load_file_buttons, draw_loading_screen
from save_manager import load_game
from data_loader import calculate_current_prices_usd

# ✅ 화면 초기화
pygame.init()
screen = pygame.display.set_mode((LAYOUT["screen"]["width"], LAYOUT["screen"]["height"]))
pygame.display.set_caption("Stock Simulator")

menu_buttons = {}
running = True

while running:
    if game_mode == "menu":
        menu_buttons = draw_main_menu(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_buttons["new"].collidepoint(event.pos):
                    # ✅ New Game → 로딩 화면 표시
                    for i in range(20):  # 약 2초
                        draw_loading_screen(screen, i)
                        pygame.time.delay(100)

                    init_game()
                    game_mode = "playing"

                elif menu_buttons["load"].collidepoint(event.pos):
                    game_mode = "load_menu"

    elif game_mode == "load_menu":
        draw_load_file_buttons(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                from game_state import load_file_buttons
                for file, load_rect, del_rect in load_file_buttons:
                    if load_rect.collidepoint(event.pos):
                        # ✅ Load → 로딩 화면
                        for i in range(20):
                            draw_loading_screen(screen, i)
                            pygame.time.delay(100)

                        print(f"📂 Loading: {file}")
                        data = load_game(file)
                        init_game()

                        # ✅ 환율 기준 현재 주가 계산 반영
                        calculate_current_prices_usd(data["simulation_date_list"])

                        from game_state import current_day_index, time_indices, portfolio, profit_history, news_log
                        current_day_index = data["current_day_index"]
                        time_indices.update(data["time_indices"])
                        portfolio.update(data["portfolio"])
                        profit_history.clear()
                        profit_history.extend(data["profit_history"])
                        news_log.clear()
                        news_log.extend(data["news_log"])

                        game_mode = "playing"
                        break

                    elif del_rect.collidepoint(event.pos):
                        from save_manager import delete_game
                        delete_game(file)
                        break

    elif game_mode == "playing":
        main_loop(screen)
        running = False
