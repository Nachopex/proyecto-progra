import os

import pygame
import json
from src.ui.components import Button
from src.config import *
from src.nonogram import Nonogram

class GameScreen:
    def __init__(self, game):
        self.game = game
        self.nonogram = None

        self.buttons = [
            Button("Hint", 650, 100, BUTTON_WIDTH, BUTTON_HEIGHT, self.get_hint),
            Button("Undo", 650, 160, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.undo),
            Button("Redo", 650, 220, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.redo),
            Button("Save", 650, 280, BUTTON_WIDTH, BUTTON_HEIGHT, self.game.save_game),
            Button("Menu", 650, 340, BUTTON_WIDTH, BUTTON_HEIGHT, self.return_to_menu)
        ]
        self.load_player_progress()

    def load_player_progress(self):
        try:
            with open("data/player_progress.json", "r") as f:
                self.player_progress = json.load(f)
        except FileNotFoundError:
            self.player_progress = {
                "easy": {},
                "medium": {},
                "hard": {}
            }

    def save_player_progress(self):
        with open("data/player_progress.json", "w") as f:
            json.dump(self.player_progress, f, indent=2)

    def handle_event(self, event):
        self.nonogram=self.game.nonogram

        if self.nonogram is None:
            print("Error: Nonograma no inicializado.")
            print(f"self.nonogram: {self.nonogram}")
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x = (x - self.nonogram.grid_offset[0]) // self.nonogram.cell_size
            grid_y = (y - self.nonogram.grid_offset[1]) // self.nonogram.cell_size
            if 0 <= grid_x < self.nonogram.cols and 0 <= grid_y < self.nonogram.rows:
                self.nonogram.toggle_cell(grid_y, grid_x)

        for button in self.buttons:
            button.handle_event(event)

    def update(self):
        if self.nonogram is not None and self.nonogram.is_solved():
            self.update_player_progress()


    def update_player_progress(self):
        level_key = f"level{self.game.current_level}"
        difficulty = self.get_level_difficulty()
        self.player_progress[difficulty][level_key] = True
        self.save_player_progress()

    def get_level_difficulty(self):
        if 1 <= 20: #self.game.current_level
            return "easy"
        elif 1 <= 40: #self.game.current_level
            return "medium"
        else:
            return "hard"

    def draw(self, screen):
        screen.fill(WHITE)
        if self.nonogram is not None:
            self.draw_grid(screen)
            self.draw_clues(screen)
            self.draw_timer(screen)
        else:
            font = pygame.font.Font(None, 36)
            message = font.render("No se cargó nivel.", True, (255, 0, 0))
            screen.blit(message, (300, 300))

        for button in self.buttons:
            button.draw(screen)

    def draw_grid(self, screen):
        self.nonogram.draw_grid(screen)

    def draw_clues(self, screen):
        font = pygame.font.Font(None, 24)
        for i, row_clue in enumerate(self.nonogram.row_clues):
            text = " ".join(map(str, row_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] - 80, GRID_OFFSET[1] + i * CELL_SIZE + 5))

        for i, col_clue in enumerate(self.nonogram.col_clues):
            text = "\n".join(map(str, col_clue))
            rendered = font.render(text, True, BLACK)
            screen.blit(rendered, (GRID_OFFSET[0] + i * CELL_SIZE + 5, GRID_OFFSET[1] - 80))

    def draw_timer(self, screen):
        font = pygame.font.Font(None, 36)
        timer_text = f"Time: {self.game.timer.get_time():.1f}s"
        rendered = font.render(timer_text, True, BLACK)
        screen.blit(rendered, (650, 50))

    def get_hint(self):
        hint = self.game.get_hint()
        if hint:
            row, col, value = hint
            self.nonogram.player_grid[row][col] = value

    def return_to_menu(self):
        self.game.set_screen('menu')

