import random
from typing import Tuple

import numpy as np

from constants import MazeConstants


class MazeEnv:
    # an array to store the environment cells
    env = np.NaN
    # the starting point of the agent
    start_point = None, None
    # the finishing point or the goal state that the agent must reach
    finish_point = None, None

    def init(self, width: int, height: int):
        pass

    def get_env(self) -> np.ndarray:
        return self.env

    def get_row_size(self) -> int:
        return self.get_env().shape[0]

    def get_col_size(self) -> int:
        return self.get_env().shape[1]

    def is_wall(self, row: int, column: int) -> bool:
        return self.get_env()[row, column] == MazeConstants.WALL

    def is_empty(self, row: int, column: int) -> bool:
        return not self.is_fill(row, column) and not self.is_wall(row, column)

    def is_fill(self, row: int, column: int) -> bool:
        return self.get_env()[row, column] == MazeConstants.FILL

    def is_start(self, row: int, column: int) -> bool:
        return self.get_env()[row, column] == MazeConstants.START

    def is_finish(self, row: int, column: int) -> bool:
        return self.get_env()[row, column] == MazeConstants.FINISH

    def init_start_point(self):
        self.start_point = self.get_random_empty_point()
        self.get_env()[self.start_point[0], self.start_point[1]] = MazeConstants.START

    def get_start_point(self) -> Tuple[int, int]:
        return self.start_point

    def init_finish_point(self):
        self.finish_point = self.get_random_empty_point()
        self.get_env()[self.finish_point[0], self.finish_point[1]] = MazeConstants.FINISH

    def get_finish_point(self):
        return self.finish_point

    # this function selects one random point in the environment that is empty
    def get_random_empty_point(self) -> Tuple[int, int]:
        empty_arrays = np.where(self.get_env() == MazeConstants.EMPTY)
        random_row = random.randint(0, empty_arrays[0].size - 1)
        random_col = random.randint(0, empty_arrays[0].size - 1)
        return empty_arrays[0][random_row], empty_arrays[1][random_col]

    def fill(self, row: int, column: int):
        self.get_env()[row, column] = MazeConstants.FILL

    # this function returns all the cells that are filled
    def get_filled_points(self) -> set:
        filled_array = np.where(self.get_env() == MazeConstants.FILL)
        filled_set = set()
        filled_set.add(self.get_start_point())
        for index, value in enumerate(filled_array[0]):
            filled_set.add((value, filled_array[1][index]))
        return filled_set

    # this function considers a cell as neighbour if it is empty
    def get_neighbours(self, row: int, column: int) -> list:
        neighbours = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) == abs(j):
                    continue
                if self.is_empty(row + i, column + j):
                    neighbours.append((row + i, column + j))
        return neighbours

    # this function considers a cell as neighbour if it is not wall
    def get_neighbours_custom(self, row: int, column: int) -> list:
        neighbours = list()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) == abs(j):
                    continue
                if not self.is_wall(row + i, column + j):
                    neighbours.append((row + i, column + j))
        return neighbours

    # this function returns list of all possible neighbours in the whole environment
    def get_all_neighbours(self) -> set:
        filled_points = self.get_filled_points()
        neighbours = set()
        for filled_point in filled_points:
            one_point_neighbours = self.get_neighbours(filled_point[0], filled_point[1])
            for neighbour in one_point_neighbours:
                neighbours.add(neighbour)
        return neighbours
