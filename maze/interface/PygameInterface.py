import pygame

from env.MazeEnv import MazeEnv
from interface.MazeInterface import MazeInterface
from solver.MazeSolver import MazeSolver


class PygameInterface(MazeInterface):

    # using different colors for each type of data in the environment
    EMPTY_COLOR = (255, 255, 255)
    WALL_COLOR = (0, 0, 0, 0)
    FILL_COLOR = (255, 0, 0)
    START_COLOR = (0, 255, 0)
    FINISH_COLOR = (0, 0, 255)

    # More delays means slower animation
    DELAY_PER_ACTION = 50

    maze_env = None
    maze_solver = None
    square_size = None
    surface = None
    screen = None

    def __init__(self, maze_env: MazeEnv, maze_solver: MazeSolver):
        pygame.init()
        row = maze_env.get_row_size()
        column = maze_env.get_col_size()
        # The size of each box in the output is generated dynamically.
        # If we need to show a lot of boxes in the screen, then boxes must be small
        size_per_box = int(1024 / max(row, column))
        screen = pygame.display.set_mode((row * size_per_box, column * size_per_box), 0, 32)
        surface = pygame.Surface(screen.get_size())

        self.maze_env = maze_env
        self.maze_solver = maze_solver
        self.screen = screen
        self.surface = surface.convert()
        self.square_size = size_per_box

    def animate(self):
        self.draw_board()
        self.update_board()

    def get_color(self, row_index, col_index):
        # The color of the box will be selected according to the value of the index in the 2D array
        if self.maze_env.is_wall(row_index, col_index):
            return self.WALL_COLOR
        elif self.maze_env.is_fill(row_index, col_index):
            return self.FILL_COLOR
        elif self.maze_env.is_start(row_index, col_index):
            return self.START_COLOR
        elif self.maze_env.is_finish(row_index, col_index):
            return self.FINISH_COLOR
        else:
            return self.EMPTY_COLOR

    def draw_board(self):
        # for each index of the 2D array, we create a small square according to the screen size
        for row_index, row_value in enumerate(self.maze_env.get_env()):
            for col_index, col_value in enumerate(row_value):
                left_x = self.get_left_x(row_index, self.square_size)
                left_y = self.get_left_y(col_index, self.square_size)
                color = self.get_color(row_index, col_index)
                rect = self.get_square(left_x, left_y, self.square_size)
                self.draw(self.screen, self.surface, color, rect)

    def update_board(self):
        # we can continue showing the surface as long as the solver process is not finished
        while not self.maze_solver.get_finished():
            if self.maze_solver.get_reset():
                self.maze_env = self.maze_solver.maze_env
                self.maze_solver.undo_reset()
                self.draw_board()
            # tick function of all solvers will return the next action of the agent
            head_row, head_col = self.maze_solver.tick()
            left_x = self.get_left_x(head_row, self.square_size)
            left_y = self.get_left_y(head_col, self.square_size)
            color = self.get_color(head_row, head_col)
            rect = pygame.Rect((left_x, left_y), (self.square_size, self.square_size))
            pygame.draw.rect(self.surface, color, rect)
            self.screen.blit(self.surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(self.DELAY_PER_ACTION)

    @staticmethod
    def draw(screen, surface, color, rect):
        pygame.draw.rect(surface, color, rect)
        screen.blit(surface, (0, 0))
        pygame.display.update()

    @staticmethod
    def get_left_x(row_index, size_per_box):
        return row_index * size_per_box

    @staticmethod
    def get_left_y(col_index, size_per_box):
        return col_index * size_per_box

    @staticmethod
    def get_square(left_x, left_y, size):
        return pygame.Rect((left_x, left_y), (size, size))
