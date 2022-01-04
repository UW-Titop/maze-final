import random
from typing import Tuple

from env.MazeEnv import MazeEnv
from solver.MazeSolver import MazeSolver


class BestFirstMazeSolver(MazeSolver):

    def init(self, env: MazeEnv):
        self.maze_env = env

    def select_next(self) -> Tuple[int, int]:
        # getting the position of the goal state
        finish_point = self.maze_env.get_finish_point()
        finish_row = finish_point[0]
        finish_col = finish_point[1]

        # getting list of all possible neighbours
        neighbours = self.maze_env.get_all_neighbours()
        if len(neighbours) == 0:
            return -1, -1

        # finding the neighbour with the smallest f(n) function
        next_point = random.sample(neighbours, 1)
        next_row = next_point[0][0]
        next_col = next_point[0][1]
        for neighbour in neighbours:
            neighbour_row = neighbour[0]
            neighbour_col = neighbour[1]
            # for the best first function, we only need to find the smallest heuristic, not smallest f(n)
            if self.get_distance(neighbour_row, neighbour_col, finish_row, finish_col) < \
                    self.get_distance(next_row, next_col, finish_row, finish_col):
                next_row = neighbour_row
                next_col = neighbour_col
        return next_row, next_col

    @staticmethod
    def get_distance(x_row, x_col, y_row, y_col):
        # returning the absolute distance between two states as heuristic function
        return abs(x_row - y_row) + abs(x_col - y_col)
