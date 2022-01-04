import numpy as np

from constants import MazeConstants
from env.MazeEnv import MazeEnv
import random


class KruskalMazeEnv(MazeEnv):
    # storing height of the generated environment
    row = 0
    # storing width of the generated environment
    column = 0

    def init(self, row, column):
        self.row = row
        self.column = column
        # all grids are initially WALL
        env = np.full((row, column), MazeConstants.WALL)
        # One among the walls must become empty
        for i in range(row):
            if i % 2 == 0:
                continue
            else:
                env[i, :] = MazeConstants.EMPTY
        for i in range(column):
            if i % 2 == 1:
                continue
            else:
                env[:, i] = MazeConstants.WALL
        env[:, 0] = MazeConstants.WALL
        env[:, column - 1] = MazeConstants.WALL
        env[row - 1, :] = MazeConstants.WALL
        env[0, :] = MazeConstants.WALL
        self.set_env(env)
        self.create()
        self.init_start_point()
        self.init_finish_point()

    def set_env(self, env):
        self.env = env

    def get_env(self):
        return self.env

    # this function returns a set of all walls in the environment
    def get_wall_set(self):
        wall_arrays = np.where(self.env == MazeConstants.WALL)
        wall_set = set()
        for index, value in enumerate(wall_arrays[0]):
            r1 = value
            c1 = wall_arrays[1][index]
            if r1 == 0 or r1 == self.row - 1 or c1 == 0 or c1 == self.column - 1:
                continue
            if r1 % 2 == 0 and c1 % 2 == 0:
                continue
            wall_set.add((r1, c1))
        return wall_set

    def get_empty_set(self):
        empty_arrays = np.where(self.env == MazeConstants.EMPTY)
        empty_set = list(set(()))
        for index, value in enumerate(empty_arrays[0]):
            x_set = set()
            x_set.add((value, empty_arrays[1][index]))
            empty_set.append(x_set)
        return empty_set

    # each wall has two neighbours at most. The calculation when the wall is horizontal or vertial is different.
    def get_wall_neighbours(self, selected_wall, selected_wall_row, selected_wall_col):
        if self.is_horizontal(selected_wall):
            up_neighbour_row = selected_wall_row - 1
            down_neighbour_row = selected_wall_row + 1
            first_neighbour = (up_neighbour_row, selected_wall_col)
            second_neighbour = (down_neighbour_row, selected_wall_col)
        else:
            left_neighbour_col = selected_wall_col - 1
            right_neighbour_col = selected_wall_col + 1
            first_neighbour = (selected_wall_row, left_neighbour_col)
            second_neighbour = (selected_wall_row, right_neighbour_col)
        return first_neighbour, second_neighbour

    @staticmethod
    def get_set_of_neighbours(first_neighbour, second_neighbour, empty_set):
        first_set = set()
        second_set = set()
        for my_set in empty_set:
            if first_neighbour in my_set:
                first_set = my_set
            if second_neighbour in my_set:
                second_set = my_set
        return first_set, second_set

    def modify_env(self, empty_set, selected_wall_row, selected_wall_col, first_set, second_set):
        if len(first_set) > 0 and first_set == second_set:
            return
        else:
            self.env[selected_wall_row, selected_wall_col] = MazeConstants.EMPTY
            if first_set in empty_set:
                empty_set.remove(first_set)
            if second_set in empty_set:
                empty_set.remove(second_set)
            empty_set.append(first_set.union(second_set))

    def create(self):
        wall_set = self.get_wall_set()
        empty_set = self.get_empty_set()

        while len(wall_set) > 0:
            selected_wall = random.choice(tuple(wall_set))
            wall_set.remove(selected_wall)
            selected_wall_row = selected_wall[0]
            selected_wall_col = selected_wall[1]

            first_neighbour, second_neighbour = \
                self.get_wall_neighbours(selected_wall, selected_wall_row, selected_wall_col)
            first_set, second_set = self.get_set_of_neighbours(first_neighbour, second_neighbour, empty_set)
            self.modify_env(empty_set, selected_wall_row, selected_wall_col, first_set, second_set)

    @staticmethod
    def is_horizontal(selected_wall):
        return selected_wall[0] % 2 == 0
