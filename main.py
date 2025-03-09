import pygame
from game_logic import GoGame
from graphics import GoGraphics
from constants import BLACK, WHITE, BOARD_BROWN, BOARD_WIDTH, BOARD_BORDER


def show_menu(screen, font):
    """Отображает главное меню и возвращает выбор пользователя."""
    screen.fill(BOARD_BROWN)  # Заливаем экран цветом доски

    # Текст меню
    title = font.render("Выберите размер доски:", True, BLACK)
    option1 = font.render("1. 9x9", True, BLACK)
    option2 = font.render("2. 13x13", True, BLACK)
    option3 = font.render("3. 19x19", True, BLACK)
    option4 = font.render("4. Выход", True, BLACK)

    # Позиции текста
    screen.blit(title, (BOARD_BORDER, BOARD_BORDER))
    screen.blit(option1, (BOARD_BORDER, BOARD_BORDER + 50))
    screen.blit(option2, (BOARD_BORDER, BOARD_BORDER + 100))
    screen.blit(option3, (BOARD_BORDER, BOARD_BORDER + 150))
    screen.blit(option4, (BOARD_BORDER, BOARD_BORDER + 200))

    pygame.display.flip()

    # Ожидание выбора пользователя
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None  # Выход из игры
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 9
                if event.key == pygame.K_2:
                    return 13
                if event.key == pygame.K_3:
                    return 19
                if event.key == pygame.K_4:
                    return None  # Выход из игры


def main():
    """Основной цикл игры."""
    pygame.init()
    screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
    font = pygame.font.SysFont("arial", 30)

    # Отображение меню
    size = show_menu(screen, font)
    if size is None:
        print("Выход из игры.")
        pygame.quit()
        return

    # Инициализация игры и графики
    game = GoGame(size)
    graphics = GoGraphics(game)

    while True:
        graphics.draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                # Проверка, нажата ли кнопка "Выход"
                if graphics.exit_button.collidepoint(x, y):
                    pygame.quit()
                    return
                # Размещение камня
                col, row = graphics.get_board_coords(x, y)
                if not game.place_stone(col, row):
                    print("Недопустимый ход!")
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:  # Пропуск хода
                    game.black_turn = not game.black_turn
                if event.key == pygame.K_u:  # Отмена хода
                    game.undo_move()


if __name__ == "__main__":
    main()