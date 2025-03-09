import unittest
import numpy as np
from game_logic import GoGame


class TestGoGame(unittest.TestCase):
    def setUp(self):
        """Инициализация игры перед каждым тестом."""
        self.game = GoGame(size=9)

    def test_initial_board(self):
        """Проверка начального состояния доски."""
        self.assertEqual(self.game.board.shape, (9, 9))  # Доска 9x9
        self.assertTrue(np.all(self.game.board == 0))  # Все клетки пусты

    def test_place_stone_valid(self):
        """Проверка допустимого хода."""
        self.assertTrue(self.game.place_stone(0, 0))  # Ход в углу доски
        self.assertEqual(self.game.board[0, 0], 1)  # Черный камень размещен

    def test_place_stone_invalid(self):
        """Проверка недопустимого хода."""
        self.game.place_stone(0, 0)  # Размещаем камень
        self.assertFalse(self.game.place_stone(0, 0))  # Ход в занятую клетку

    def test_capture_stones(self):
        """Проверка захвата камней."""
        # Черные окружают белый камень
        self.game.place_stone(1, 0)  # Черный
        self.game.place_stone(0, 1)  # Черный
        self.game.place_stone(1, 1)  # Белый
        self.game.place_stone(0, 2)  # Черный
        self.game.place_stone(1, 2)  # Черный

        # Белый камень должен быть захвачен
        self.assertEqual(self.game.board[1, 1], 0)
        self.assertEqual(self.game.prisoners['black'], 1)  # Черные захватили 1 камень

    def test_has_no_liberties(self):
        """Проверка наличия либерти у группы."""
        # Черные окружают белый камень
        self.game.place_stone(1, 0)  # Черный
        self.game.place_stone(0, 1)  # Черный
        self.game.place_stone(1, 1)  # Белый
        self.game.place_stone(0, 2)  # Черный
        self.game.place_stone(1, 2)  # Черный

        # Проверка, что у белого камня нет либерти
        group = list(self.game.get_stone_groups('white'))[0]
        self.assertTrue(self.game.has_no_liberties(group))

    def test_ko_rule(self):
        """Проверка правила ко."""
        # Черные и белые по очереди создают повторяющуюся позицию
        self.game.place_stone(0, 0)  # Черный
        self.game.place_stone(1, 0)  # Белый
        self.game.place_stone(1, 1)  # Черный
        self.game.place_stone(0, 1)  # Белый
        self.game.place_stone(0, 0)  # Черный (нарушение правила ко)

        # Ход должен быть отклонен
        self.assertEqual(self.game.board[0, 0], 0)

    def test_calculate_score(self):
        """Проверка подсчета очков."""
        # Черные захватывают 2 камня
        self.game.place_stone(0, 0)  # Черный
        self.game.place_stone(1, 0)  # Черный
        self.game.place_stone(0, 1)  # Белый
        self.game.place_stone(1, 1)  # Белый
        self.game.place_stone(0, 2)  # Черный
        self.game.place_stone(1, 2)  # Черный

        # Подсчет очков
        scores = self.game.calculate_score()
        self.assertEqual(scores['black'], 2)  # Черные захватили 2 камня
        self.assertEqual(scores['white'], 6.5)  # Белые с коми

    def test_undo_move(self):
        """Проверка отмены хода."""
        self.game.place_stone(0, 0)  # Черный
        self.game.undo_move()  # Отменяем ход
        self.assertEqual(self.game.board[0, 0], 0)  # Камень удален


if __name__ == "__main__":
    unittest.main()