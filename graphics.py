import pygame
from pygame import gfxdraw
import itertools
from constants import BLACK, WHITE, BOARD_BROWN, BOARD_WIDTH, BOARD_BORDER, STONE_RADIUS, DOT_RADIUS, TURN_POS, \
    SCORE_POS


class GoGraphics:
    def __init__(self, game):
        """
        Инициализация графического интерфейса.

        :param game: Объект игры (GoGame).
        """
        self.game = game
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        self.font = pygame.font.SysFont("arial", 30, bold=True)  # Улучшенный шрифт

        # Загрузка текстур
        self.wood_texture = pygame.image.load("wood_texture.jpg")  # Текстура дерева для доски
        self.wood_texture = pygame.transform.scale(self.wood_texture, (BOARD_WIDTH, BOARD_WIDTH))

        # Кнопка "Выход"
        self.exit_button = pygame.Rect(BOARD_WIDTH - 150, 10, 140, 40)  # Позиция и размер кнопки
        self.exit_font = pygame.font.SysFont("arial", 20, bold=True)
        self.exit_text = self.exit_font.render("Выход", True, WHITE)

    def draw_board(self):
        """Отрисовывает доску, сетку, камни и кнопку "Выход"."""
        # Фон доски с текстурой дерева
        self.screen.blit(self.wood_texture, (0, 0))

        # Отрисовка сетки
        inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (self.game.size - 1)
        for i in range(self.game.size):
            # Вертикальные линии
            start_x = BOARD_BORDER + i * inc
            start_y = BOARD_BORDER
            end_x = start_x
            end_y = BOARD_WIDTH - BOARD_BORDER
            pygame.draw.line(self.screen, BLACK, (start_x, start_y), (end_x, end_y), 2)  # Толщина линии 2

            # Горизонтальные линии
            start_x = BOARD_BORDER
            start_y = BOARD_BORDER + i * inc
            end_x = BOARD_WIDTH - BOARD_BORDER
            end_y = start_y
            pygame.draw.line(self.screen, BLACK, (start_x, start_y), (end_x, end_y), 2)  # Толщина линии 2

        # Отрисовка направляющих точек
        guide_dots = [3, self.game.size // 2, self.game.size - 4]
        for col, row in itertools.product(guide_dots, guide_dots):
            x, y = self.get_pixel_coords(col, row)
            gfxdraw.aacircle(self.screen, x, y, DOT_RADIUS, BLACK)
            gfxdraw.filled_circle(self.screen, x, y, DOT_RADIUS, BLACK)

        # Отрисовка камней
        for x, y in itertools.product(range(self.game.size), repeat=2):
            px, py = self.get_pixel_coords(x, y)
            if self.game.board[x, y] == 1:
                self.draw_stone(px, py, BLACK)
            elif self.game.board[x, y] == 2:
                self.draw_stone(px, py, WHITE)

        # Отрисовка текста
        score_msg = f"Захвачено черных: {self.game.prisoners['black']}  Захвачено белых: {self.game.prisoners['white']}"
        txt = self.font.render(score_msg, True, BLACK)
        self.screen.blit(txt, SCORE_POS)
        turn_msg = f"Ход {'черных' if self.game.black_turn else 'белых'}. Кликните, чтобы поставить камень, P - пропуск хода, U - отмена."
        txt = self.font.render(turn_msg, True, BLACK)
        self.screen.blit(txt, TURN_POS)

        # Отрисовка кнопки "Выход"
        pygame.draw.rect(self.screen, (200, 0, 0), self.exit_button)  # Красный прямоугольник
        self.screen.blit(self.exit_text, (self.exit_button.x + 10, self.exit_button.y + 10))  # Текст на кнопке

        pygame.display.flip()

    def draw_stone(self, x, y, color):
        """
        Отрисовывает камень на доске с эффектом тени.

        :param x: Координата x в пикселях.
        :param y: Координата y в пикселях.
        :param color: Цвет камня.
        """
        # Тень камня
        shadow_offset = 3
        gfxdraw.aacircle(self.screen, x + shadow_offset, y + shadow_offset, STONE_RADIUS, (50, 50, 50))
        gfxdraw.filled_circle(self.screen, x + shadow_offset, y + shadow_offset, STONE_RADIUS, (50, 50, 50))

        # Сам камень
        gfxdraw.aacircle(self.screen, x, y, STONE_RADIUS, color)
        gfxdraw.filled_circle(self.screen, x, y, STONE_RADIUS, color)

    def get_pixel_coords(self, col, row):
        """
        Преобразует координаты доски в пиксели.

        :param col: Номер столбца.
        :param row: Номер строки.
        :return: Координаты (x, y) в пикселях.
        """
        inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (self.game.size - 1)
        x = int(BOARD_BORDER + col * inc)
        y = int(BOARD_BORDER + row * inc)
        return x, y

    def get_board_coords(self, x, y):
        """
        Преобразует координаты пикселей в координаты доски.

        :param x: Координата x в пикселях.
        :param y: Координата y в пикселях.
        :return: Координаты (col, row) на доске.
        """
        inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (self.game.size - 1)
        col = int(round((x - BOARD_BORDER) / inc))
        row = int(round((y - BOARD_BORDER) / inc))
        return col, row