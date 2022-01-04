import copy
import random

from solver.MazeSolver import MazeSolver


class HeadRandomMazeSolver(MazeSolver):

    # storing list of all steps
    body = None

    def init(self, maze_env):
        self.maze_env = maze_env

        start_point = self.maze_env.get_start_point()
        self.body = list()
        self.body.append((start_point[0], start_point[1]))

    def select_next(self):
        # getting list of all neighbours according to the last action of the agent, which is located in body[-1]
        neighbours = self.maze_env.get_neighbours(self.body[-1][0], self.body[-1][1])
        if len(neighbours) == 0:
            # we must remove if the selected neighbour does not have any neighbours
            del self.body[-1]
            # calling the same function recursively until finding a state with neighbours
            return self.select_next()
        else:
            # since this algorithm works randomly, we select one of the neighbours completely randomly
            next_choice = random.choice(neighbours)
            # the selected neighbour must be added to the body because we need to have it for the next step
            self.body.append(next_choice)
            return next_choice

