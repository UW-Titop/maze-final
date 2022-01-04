from typing import Tuple

from env.MazeEnv import MazeEnv


class MazeSolver:
    maze_env = None
    is_finished = False
    is_successful = False
    reset = False

    def init(self, maze_env: MazeEnv):
        self.maze_env = maze_env

    def tick(self) -> Tuple[int, int]:
        next_row, next_col = self.select_next()
        if next_row == -1 and next_col == -1:
            self.finish_and_unsuccessful()
        else:
            self.maze_env.fill(next_row, next_col)
            finish_row, finish_col = self.maze_env.get_finish_point()
            if next_row == finish_row and next_col == finish_col:
                self.finish_and_successful()
        return next_row, next_col

    def select_next(self) -> Tuple[int, int]:
        raise NotImplementedError

    def get_finished(self) -> bool:
        return self.is_finished

    def get_reset(self) -> bool:
        return self.reset

    def do_reset(self):
        self.reset = True

    def undo_reset(self):
        self.reset = False

    def get_successful(self) -> bool:
        return self.is_successful

    def finish_and_successful(self):
        self.is_successful = True
        self.is_finished = True

    def finish_and_unsuccessful(self):
        self.is_successful = False
        self.is_finished = True
