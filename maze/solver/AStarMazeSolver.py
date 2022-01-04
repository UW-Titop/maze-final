import random

from env.MazeEnv import MazeEnv
from solver.MazeSolver import MazeSolver


class AStarMazeSolver(MazeSolver):

    # storing row of the head
    head_row = None
    # storing column of the head
    head_col = None
    # storing the cost function for reaching to a state
    gn = None
    # storing list of all possible choices for the future action
    neighbours = None

    def init(self, env: MazeEnv):
        self.maze_env = env

        start_point = self.maze_env.get_start_point()
        self.head_row = start_point[0]
        self.head_col = start_point[1]
        self.gn = dict()
        self.gn[(self.head_row, self.head_col)] = 0
        self.neighbours = list()

    def select_next(self):
        # getting the position of the goal state
        finish_point = self.maze_env.get_finish_point()
        finish_row = finish_point[0]
        finish_col = finish_point[1]

        # getting list of all possible neighbours for the current state
        self.neighbours += self.maze_env.get_neighbours(self.head_row, self.head_col)
        if len(self.neighbours) == 0:
            return -1, -1

        # finding the neighbour with the smallest f(n) function
        next_point = random.sample(self.neighbours, 1)
        next_row = next_point[0][0]
        next_col = next_point[0][1]
        for neighbour in self.neighbours:
            neighbour_row = neighbour[0]
            neighbour_col = neighbour[1]
            if self.get_fn(neighbour_row, neighbour_col, finish_row, finish_col) < \
                    self.get_fn(next_row, next_col, finish_row, finish_col):
                next_row = neighbour_row
                next_col = neighbour_col
        self.neighbours.remove((next_row, next_col))

        # storing the cost of selected neighbour
        self.gn[(next_row, next_col)] = self.gn[(self.head_row, self.head_col)] + 1
        # updating current head
        self.head_row = next_row
        self.head_col = next_col

        return next_row, next_col

    def get_fn(self, x_row, x_col, y_row, y_col):
        # f(n) = h(n) + g(n) = distance between current state and the goal state + cost of reaching to the current state
        return int(self.get_distance(x_row, x_col, y_row, y_col)) + int(self.gn[(self.head_row, self.head_col)])

    def get_distance(self, x_row, x_col, y_row, y_col):
        # returning the absolute distance between two states as heuristic function
        return abs(x_row - y_row) + abs(x_col - y_col)
