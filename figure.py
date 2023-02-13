from enum import StrEnum
from typing import List, Dict
import random
from point import Point
import pygame
from config import Config
import numpy as np

class FigureColor(StrEnum):
    GREEN = '#00b849'
    PINK = '#e805d9'
    BLUE = '#0541e8'
    ORANGE = '#FF5733'
    YELLOW = '#F4FF00'
    RED = '#FF0000'


class CanMove:
    points_positions: List[Point]
    shape: List[List[int]]

    def __init__(self, x: int, y: int) -> None:
        self._rotation_point = Point(x, y)

    def move_down(self) -> None:
        "Moves figure down"
        points_positions = []
        try:
            for point in self.points_positions:
                new_point = Point(point.x, point.y+1)
                points_positions.append(new_point)
            self.points_positions = points_positions
            self._rotation_point.y += 1
        except ValueError:
            return None


    def move_left(self, field: List[List[int]]) -> None:
        "Moves figure left"
        points_positions = []
        try:
            for point in self.points_positions:
                new_point = Point(point.x - 1, point.y)
                if field[new_point.y][new_point.x] != 0:
                    return None
                points_positions.append(new_point)
            self.points_positions = points_positions
            self._rotation_point.x -= 1
        except ValueError:
            return None

    def move_right(self, field: List[List[int]]) -> None:
        "Moves figure right"
        points_positions = []
        try:
            for point in self.points_positions:
                new_point = Point(point.x + 1, point.y)
                if field[new_point.y][new_point.x] != 0:
                    return None
                points_positions.append(new_point)
            self.points_positions = points_positions
            self._rotation_point.x += 1
        except ValueError:
            return None

    def rotate(self) -> None:
        "Rotates figure 90 degree"
        rotated_shape = np.rot90(self.shape)
        self.shape = rotated_shape
        self._update_points_pos_based_point(self._rotation_point)

    def _update_points_pos_based_point(self, point: Point) -> None:
        "Updates position points based on point"
        number_of_row = len(self.shape)
        number_of_col = len(self.shape[0])
        points_positions = []

        for row in range(number_of_row):
            for col in range(number_of_col):
                if self.shape[row][col] == 0:
                    continue
                try:
                    new_point = Point(point.x + col, point.y + row)
                    points_positions.append(new_point)
                except ValueError:
                    return None

        self.points_positions = points_positions


class Figure(CanMove):
    shape_name: str
    shape: List[List[int]]
    color: str
    points_positions: List[Point]

    FIGURES: Dict[str, List[List[int]]] = {'o-shaped': [[1, 1],
                                                        [1, 1]],
                                           't-shaped': [[1, 1, 1],
                                                        [0, 1, 0]],
                                           'l-shaped': [[1, 0],
                                                        [1, 0],
                                                        [1, 1]],
                                           'i-shaped': [[1],
                                                        [1],
                                                        [1]],
                                           's-shaped': [[0, 1, 1],
                                                        [1, 1, 0]],
                                           'z-shaped': [[1, 1, 0],
                                                        [0, 1, 1]],
                                           }

    def __init__(self, x: int = 3, y: int = 0) -> None:
        self.shape_name, self.shape = random.choice(list(self.FIGURES.items()))
        self.color = random.choice(list(FigureColor))
        self.points_positions = []
        self._update_points_pos_based_point(Point(3, 0))

        super().__init__(x, y)

    def draw_figure(self, screen: pygame.Surface) -> pygame.Surface:
        "Draws figure on the screen"
        for fig_point in self.points_positions:
            rect = (fig_point.x * Config.GRID_SIZE + Config.X_OFFSET,
                    fig_point.y * Config.GRID_SIZE + Config.Y_OFFSET,
                    Config.GRID_SIZE - 2,
                    Config.GRID_SIZE - 2)
            pygame.draw.rect(screen, self.color, rect)

        return screen



