import random

import pygame
import sys

# Config
WIN_SIZE = WIDTH, HEIGHT = 1280, 960
CELL_SIZE = 10
FPS = 30

# Colors
BACKGROUND_COLOR = (100, 100, 100)
CELL_COLOR = [(50, 50, 50), (245, 120, 66)]


class GameOfLife():
    def __init__(self):
        pygame.init()

        # Screen
        self.screen = pygame.display.set_mode(WIN_SIZE)
        pygame.display.set_caption('Game of Life')

        # Timing
        self.clock = pygame.time.Clock()

        # Create Cells
        self.grid_rows = HEIGHT // CELL_SIZE
        self.grid_columns = WIDTH // CELL_SIZE
        self.grid = []
        self.transfer_grid = []
        self.init_cells()
        self.randomize_cells()
        self.draw_cells()

    def init_cells(self):
        for y in range(self.grid_rows):
            row = []
            transfer_row = []
            for x in range(self.grid_columns):
                cell = Cell(x=x * (CELL_SIZE + 1), y=y * (CELL_SIZE + 1))
                row.append(cell)
                transfer_row.append(0)
            self.grid.append(row)
            self.transfer_grid.append(transfer_row)

    def draw_cells(self):
        self.screen.fill(BACKGROUND_COLOR)
        for row in self.grid:
            for cell in row:
                pygame.draw.rect(self.screen, CELL_COLOR[cell.state], (cell.x, cell.y, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

    @staticmethod
    def zero_out_grid(grid):
        for row in grid:
            for cell in row:
                cell.state = 0

    def randomize_cells(self):
        for row in self.grid:
            for cell in row:
                cell.state = random.randint(0, 1)

    def update_grid(self, new_grid):
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                self.grid[row][col].state = new_grid[row][col]

    def get_cell_state(self, r, c):
        try:
            cell_value = self.grid[r][c].state
        except:
            cell_value = 0
        return cell_value

    def get_neighbors(self, index):
        num_neighbors = 0
        num_neighbors += self.get_cell_state(index[0] - 1, index[1] - 1)
        num_neighbors += self.get_cell_state(index[0] - 1, index[1])
        num_neighbors += self.get_cell_state(index[0] - 1, index[1] + 1)
        num_neighbors += self.get_cell_state(index[0], index[1] - 1)
        num_neighbors += self.get_cell_state(index[0], index[1] + 1)
        num_neighbors += self.get_cell_state(index[0] + 1, index[1] - 1)
        num_neighbors += self.get_cell_state(index[0] + 1, index[1])
        num_neighbors += self.get_cell_state(index[0] + 1, index[1] + 1)
        return num_neighbors

    def update_generation(self):
        new_grid = self.transfer_grid.copy()

        for r in range(self.grid_rows):
            for c in range(self.grid_columns):

                num_neighbors = self.get_neighbors([r, c])

                # Game Rules
                if self.grid[r][c].state == 1:  # Alive
                    if num_neighbors < 2:  # Underpopulation
                        new_grid[r][c] = 0  # Dies
                    elif num_neighbors > 3:  # Overpopulation
                        new_grid[r][c] = 0  # Dies
                    elif num_neighbors == 2 or num_neighbors == 3:  # Moves On
                        new_grid[r][c] = 1  # Lives
                elif self.grid[r][c].state == 0:  # Dead
                    if num_neighbors == 3:  # Reproduction
                        new_grid[r][c] = 1  # Born

        self.update_grid(new_grid)
        del new_grid

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Press r to randomize cells
                if event.key == pygame.K_r:
                    self.randomize_cells()
                # Press space to toggle pause
                # Press c to clear board
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.clock.tick(FPS)
            self.handle_events()
            self.update_generation()
            self.draw_cells()


class Cell:
    def __init__(self, x, y, state=0):
        self.state = state
        self.x = x
        self.y = y


if __name__ == '__main__':
    game = GameOfLife()
    game.run()
