from __future__ import annotations
import numpy as np
import random
from dataclasses import dataclass
from enum import StrEnum
import pygame
from typing import List
from figure import Figure
from board import Board
from config import Config
from color import Color
from typing import Dict


class GameStatus(StrEnum):
    RUNNING = 'running'
    GAME_OVER = 'game_over'


class Tetris:
    _level: int
    _score: int
    _cleared_lines: int
    _field: Board
    _screen: pygame.Surface
    _figure: Figure
    _game_status: GameStatus

    lines_cleared_scores: Dict[int, int] = {1: 40,
                                            2: 100,
                                            3: 300,
                                            4: 1200}
    def __init__(self):
        self._level = 1
        self._score = 0
        self._cleared_lines = 0
        self._field = Board()
        self._screen = self._prepare_game_screen()
        self._figure = None
        self._game_status = GameStatus.RUNNING

        pygame.init()

    def _prepare_game_screen(self) -> pygame.Surface:
        "Prepares game screen based on dimensions in Config class"
        screen_width = 2 * Config.X_OFFSET + Config.COL_NUMBER * Config.GRID_SIZE
        screen_height = 2 * Config.Y_OFFSET + Config.ROW_NUMBER * Config.GRID_SIZE
        screen_dim = (screen_width, screen_height)

        screen = pygame.display.set_mode(screen_dim)
        return screen

    def _update_game_status(self) -> None:
        "Updates game status"
        if not self._field.is_empty_rows():
            self._game_status = GameStatus.GAME_OVER

    def _update_screen(self, screen: pygame.Surface) -> None:
        "Updates screen"
        self._screen = screen

    def _new_figure(self):
        "Creates new figure"
        self._figure = Figure()

    def _on_figure_collision(self):
        self._field.freeze_figure(self._figure)
        self._figure = None

    def update_score(self) -> None:
        "Updates game score and cleared lines"
        rows_cleared = self._field.clear_full_rows()
        if rows_cleared != 0:
            self._score += self.lines_cleared_scores[rows_cleared]
        self._cleared_lines += rows_cleared

    def update_level(self) -> None:
        if self._cleared_lines % 10 == 0 and self._cleared_lines != 0:
            self._level += 1
            self._cleared_lines = 0

    def _draw_level(self) -> None:
        font = pygame.font.SysFont('Calibri', 25, True, False)
        score_text = font.render(f'Level: {str(self._level)}', True, Color.WHITE)
        self._screen.blit(score_text, [25, 30])

    def _draw_score(self) -> None:
        font = pygame.font.SysFont('Calibri', 25, True, False)
        score_text = font.render(f'Score: {str(self._score)}', True, Color.WHITE)
        self._screen.blit(score_text, [25, 10])

    def _show_game_over_screen(self) -> None:
        font = pygame.font.SysFont('Calibri', 25, True, False)
        game_over_text = font.render('Game Over', True, Color.ORANGE)
        replay_text = font.render("Press Esc to replay", True, Color.ORANGE)
        self._screen.blit(game_over_text, [150, 25])
        self._screen.blit(replay_text, [105, 475])

    def _on_game_over(self) -> None:
        self._update_screen(self._field.draw_field(self._screen))
        self._show_game_over_screen()

    def _restart_game(self) -> None:
        self._game_status = GameStatus.RUNNING
        self._score = 0
        self._field.clear_field()
        self._new_figure()

    def run_game(self) -> None:
        done = False
        pressing_down = False
        clock = pygame.time.Clock()
        counter = 0

        while not done:
            counter += 1
            if counter > 1000:
                counter = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if self._figure:
                        if event.key == pygame.K_RIGHT:
                            self._figure.move_right(self._field.fields)
                        if event.key == pygame.K_LEFT:
                            self._figure.move_left(self._field.fields)
                        if event.key == pygame.K_UP:
                            self._figure.rotate()
                        if event.key == pygame.K_DOWN:
                            pressing_down = True
                    if event.key == pygame.K_ESCAPE:
                        self._restart_game()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    pressing_down = False
            self._draw_score()

            if self._game_status == GameStatus.GAME_OVER:
                continue

            self._update_screen(self._field.draw_field(self._screen))
            if not self._figure:
                self._new_figure()

            if self._field.check_vertical_collision(self._figure):
                self._on_figure_collision()
                self.update_score()
                self.update_level()
            else:
                if counter % Config.FPS_RATE == 0 or pressing_down:
                    self._figure.move_down()

            if self._figure:
                self._update_screen(self._figure.draw_figure(self._screen))

            self._update_game_status()

            if self._game_status == GameStatus.GAME_OVER:
                self._on_game_over()

            self._draw_score()
            self._draw_level()

            pygame.display.flip()
            clock.tick(Config.FPS_RATE)


if __name__ == '__main__':
    t = Tetris()
    t.run_game()
