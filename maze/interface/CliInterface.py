from env.MazeEnv import MazeEnv
from MazeInterface import MazeInterface


class CliInterface(MazeInterface):
    maze_env = MazeEnv()

    def __init__(self, maze_env):
        self.maze_env = maze_env

    def animate(self):
        for i in range(self.maze_env.get_row_size()):
            for j in range(self.maze_env.get_col_size()):
                if self.maze_env.is_empty(i, j):
                    print(" + ", end='')
                else:
                    print(" - ", end='')
            print()