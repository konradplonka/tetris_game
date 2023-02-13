from dataclasses import dataclass
from config import Config


class Point:
    x = property()
    y = property()
    _x: int
    _y: int

    def __init__(self, x=0, y=0) -> None:
        self._validate_x(x)
        self._validate_y(y)

        self._x = x
        self._y = y

    @staticmethod
    def _validate_x(x_value) -> None:
        if x_value > Config.COL_NUMBER - 1 or x_value < 0:
            raise ValueError(f'x must be in range [0; {Config.COL_NUMBER - 1}]')

    @staticmethod
    def _validate_y(y_value) -> None:
        if y_value > Config.ROW_NUMBER - 1 or y_value < 0:
            raise ValueError(f'y must be in range [0; {Config.ROW_NUMBER - 1}]')

    @x.setter
    def x(self, x_value: int) -> None:
        self._validate_x(x_value)
        self._x = x_value

    @x.getter
    def x(self) -> int:
        return self._x

    @y.setter
    def y(self, y_value: int) -> None:
        self._validate_y(y_value)
        self._y = y_value

    @y.getter
    def y(self) -> int:
        return self._y

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self._x},{self._y})'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._x},{self._y})'
