import random
import sys

import numpy as np

from constants import MazeConstants
from env.MazeEnv import MazeEnv


class DepthFirstMazeEnv(MazeEnv):

    # one cell needs to be considered as the initialization cell
    init_row = 1
    init_col = 1
    # This algorithm needs to store the visited cells to prevent duplication and infinite loops
    visited_cells = set()

    def init(self, width, height):
        # If we do not increase the recursion limit, we cannot generate big environments
        sys.setrecursionlimit(100000)

        # In the beginning, all grids of the array are walls.
        env_temp = np.full((width, height), MazeConstants.WALL)
        env_temp[self.init_row, self.init_col] = MazeConstants.EMPTY

        self.visited_cells = set()
        self.deep(env_temp, self.init_row, self.init_col)
        self.env = env_temp
        # After creating the environment, we can select empty points as start and finish points
        self.init_start_point()
        self.init_finish_point()

    def deep(self, env, row, col):
        self.visited_cells.add((row, col))
        # we need list of neighbours for the current row and col
        unvisited_neighbours = self.get_unvisited_neighbour(env, row, col)
        while len(unvisited_neighbours) > 0:
            # one of the unvisited grids will be selected randomly
            selected_neighbour = random.choice(unvisited_neighbours)
            unvisited_neighbours.remove(selected_neighbour)
            if selected_neighbour in self.visited_cells:
                continue
            wall_row = int((selected_neighbour[0] + row) / 2)
            wall_col = int((selected_neighbour[1] + col) / 2)
            self.visited_cells.add((wall_row, wall_col))
            env[wall_row, wall_col] = MazeConstants.EMPTY
            env[selected_neighbour[0], selected_neighbour[1]] = MazeConstants.EMPTY
            # depth first maze generation works recursively
            self.deep(env, selected_neighbour[0], selected_neighbour[1])

    def get_unvisited_neighbour(self, env, row, col):
        unvisited_cells = list(())
        # creating a square over the current grid and finding the neighbours that not in self.visited_cells list
        for i in range(-2, 3, 2):
            for j in range(-2, 3, 2):
                if abs(i) == abs(j):
                    continue
                neighbour_row = row + i
                neighbour_col = col + j
                if neighbour_row == row and neighbour_col == col:
                    continue
                # diagonal neighbours are not valid
                if self.not_valid_neighbour(env, neighbour_row, neighbour_col):
                    continue
                if (neighbour_row, neighbour_col) not in self.visited_cells:
                    unvisited_cells.append((neighbour_row, neighbour_col))
        return unvisited_cells

    @staticmethod
    def not_valid_neighbour(env, neighbour_row, neighbour_col):
        return neighbour_row < 1 or \
               neighbour_row >= env.shape[0] - 1 or \
               neighbour_col < 1 or \
               neighbour_col >= env.shape[1] - 1
