from config import Config
from figure import Figure
import pygame
from color import Color
from typing import List

class Board:
    fields: List[List[int]]

    def __init__(self):
        self.fields = self._generate_empty_fields()

    def _generate_empty_fields(self):
        "Generates empty field"
        field = []
        for row_num in range(Config.ROW_NUMBER):
            field_row = []
            for col_num in range(Config.COL_NUMBER):
                field_row.append(0)
            field.append(field_row)

        return field

    def clear_field(self):
        "Clears field (sets all values to 0)"
        self.fields = self._generate_empty_fields()

    def is_empty_rows(self) -> bool:
        "Checks if empty rows are available"
        is_row_empty = []
        for row in self.fields:
            is_row_empty.append(any(row))

        return not all(is_row_empty)

    def clear_full_rows(self) -> int:
        "Clears full rows in field"
        rows_cleared = 0
        for row_number, row in enumerate(self.fields):
            if all(row):
                self.fields.remove(row)
                self.fields.insert(0, [0 for col in range(Config.COL_NUMBER)])
                rows_cleared += 1
        return rows_cleared

    def freeze_figure(self, figure: Figure) -> None:
        "Freezes figure on field"
        for point in figure.points_positions:
            self.fields[point.y][point.x] = figure.color

    def draw_field(self, screen: pygame.Surface) -> pygame.Surface:
        "Draws field on the screen"
        screen.fill(Color.BLACK)
        for row_num in range(Config.ROW_NUMBER):
            for col_num in range(Config.COL_NUMBER):
                rect = (Config.X_OFFSET + Config.GRID_SIZE * col_num,
                        Config.Y_OFFSET + Config.GRID_SIZE * row_num,
                        Config.GRID_SIZE,
                        Config.GRID_SIZE)
                if self.fields[row_num][col_num] != 0:
                    color = self.fields[row_num][col_num]
                    pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, Color.GRAY, rect, 1)

        return screen

    def check_vertical_collision(self, figure: Figure) -> bool:
        "Checks if current figure has horizontal collision with existing figures on the field"
        for point in figure.points_positions:
            is_height_border_exceeded = point.y == Config.ROW_NUMBER - 1

            if is_height_border_exceeded:
                return True

            is_field_not_empty = self.fields[point.y + 1][point.x] != 0

            if is_field_not_empty:
                return True

        return False

    def check_horizontal_collision(self, figure: Figure, move: str) -> bool:
        "Checks if current figure has vertical collision with existing figures on the field"
        moves = ('left', 'right')
        if move not in moves:
            raise ValueError(f'{move} not in {moves}')

        for point in figure.points_positions:
            if move == 'left':
                is_field_on_left_not_empty = self.fields[point.y][point.x - 1] != 0
                if is_field_on_left_not_empty:
                    return False

            if move == 'right':
                is_field_on_left_not_empty = self.fields[point.y][point.x + 1] != 0
                if is_field_on_left_not_empty:
                    return False

            return True






