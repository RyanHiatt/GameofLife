import random
import pygame
import sys


class GameOfLife():
    def __init__(self, window_width=1280, window_height=720, cell_size=10, fps=30):
        """
        :param window_width: default 1280
        :param window_height: default 720
        :param cell_size: default 10
        :param fps: default 30
        """
        pygame.init()
        pygame.font.init()

        # Screen
        self.window_size = self.width, self.height = window_width, window_height
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption('Game of Life')

        # Timing
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.paused = False

        # Colors
        self.background_color = (100, 100, 100)
        self.cell_color = [(50, 50, 50), (245, 120, 66)]
        self.font_color = (255, 255, 255)

        # Fonts
        self.my_font = pygame.font.SysFont('Comic Sans', 100)

        # Create Cells and Grids
        self.cell_size = cell_size
        self.grid_rows = self.height // self.cell_size
        self.grid_columns = self.width // self.cell_size
        self.grid = []
        self.transfer_grid = []
        self.init_cells()
        self.randomize_cells()
        self.draw_cells()

    def init_cells(self):
        for y in range(self.grid_rows):  # Rows
            row = []
            transfer_row = []
            for x in range(self.grid_columns):  # Columns
                cell = Cell(x=x * (self.cell_size + 1), y=y * (self.cell_size + 1))  # Instantiate Cell Object
                row.append(cell)
                transfer_row.append(0)
            self.grid.append(row)
            self.transfer_grid.append(transfer_row)  # Equivalent sized matrix of zeros

    def draw_cells(self):
        self.screen.fill(self.background_color)
        for row in self.grid:
            for cell in row:
                pygame.draw.rect(self.screen, self.cell_color[cell.state],
                                 (cell.x, cell.y, self.cell_size, self.cell_size))

    def zero_out_grid(self):
        for row in self.grid:
            for cell in row:
                cell.state = 0

    def randomize_cells(self):
        for row in self.grid:
            for cell in row:
                cell.state = random.randint(0, 1)

    def get_cell_state(self, r, c):
        """
        :param r: row index
        :param c: column index
        :return state of cell:
        """
        try:
            cell_value = self.grid[r][c].state
        except IndexError:
            cell_value = 0
        return cell_value

    def get_neighbors(self, index):
        num_neighbors = 0
        num_neighbors += self.get_cell_state(index[0] - 1, index[1] - 1)  # top left
        num_neighbors += self.get_cell_state(index[0] - 1, index[1])  # top center
        num_neighbors += self.get_cell_state(index[0] - 1, index[1] + 1)  # top right
        num_neighbors += self.get_cell_state(index[0], index[1] - 1)  # left
        num_neighbors += self.get_cell_state(index[0], index[1] + 1)  # right
        num_neighbors += self.get_cell_state(index[0] + 1, index[1] - 1)  # bottom left
        num_neighbors += self.get_cell_state(index[0] + 1, index[1])  # bottom center
        num_neighbors += self.get_cell_state(index[0] + 1, index[1] + 1)  # bottom right
        return num_neighbors

    def update_generation(self):
        # new_grid = self.transfer_grid.copy()
        new_grid = [[0 for col in range(self.grid_columns)] for row in range(self.grid_rows)]

        for r in range(self.grid_rows):
            for c in range(self.grid_columns):

                num_neighbors = self.get_neighbors([r, c])

                # Game Rules
                if self.grid[r][c].state == 1:  # Currently Alive
                    if num_neighbors < 2:  # Rule Underpopulation
                        new_grid[r][c] = 0  # Dies
                    elif num_neighbors > 3:  # Rule Overpopulation
                        new_grid[r][c] = 0  # Dies
                    elif num_neighbors == 2 or num_neighbors == 3:  # Rule Moves On
                        new_grid[r][c] = 1  # Lives
                elif self.grid[r][c].state == 0:  # Currently Dead
                    if num_neighbors == 3:  # Rule Reproduction
                        new_grid[r][c] = 1  # Born

        self.update_grid(new_grid)
        del new_grid

    def update_grid(self, new_grid):
        """
        :param new_grid:
        :return:
        """
        # Update states of all cells
        for row in range(self.grid_rows):
            for col in range(self.grid_columns):
                self.grid[row][col].state = new_grid[row][col]

    def draw_pause(self):
        text = self.my_font.render('Paused', True, self.font_color)  # Set word
        text_rect = text.get_rect()  # Get the word box
        text_rect.center = (self.width // 2, self.height // 2)  # Center word on screen
        self.screen.blit(text, text_rect)  # Display word

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # Press r to randomize cells
                if event.key == pygame.K_r:
                    print('Cells Randomized')
                    self.randomize_cells()
                # Press c to clear board
                elif event.key == pygame.K_c:
                    print('Grid Cleared')
                    self.zero_out_grid()
                # Press space to toggle pause
                elif event.key == pygame.K_SPACE:
                    if not self.paused:  # Pause Game
                        print('Game Paused')
                        self.paused = True
                        # self.draw_pause()
                    elif self.paused:  # Unpause Game
                        print('Game Unpause')
                        self.paused = False

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.clock.tick(self.fps)
            self.handle_events()
            if not self.paused:
                self.update_generation()
                self.draw_cells()
            elif self.paused:
                self.draw_pause()
            pygame.display.flip()


class Cell:
    def __init__(self, x, y, state=0):
        """
        :param x: x coordinate
        :param y: y coordinate
        :param state: default 0
        """
        self.state = state
        self.x = x
        self.y = y


if __name__ == '__main__':

    game = GameOfLife()
    game.run()
