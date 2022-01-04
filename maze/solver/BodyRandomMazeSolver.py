import random

from typing import Tuple

from solver.MazeSolver import MazeSolver
from env.MazeEnv import MazeEnv


class BodyRandomMazeSolver(MazeSolver):

    # storing all steps of the agent
    body = None

    def init(self, env: MazeEnv):
        self.maze_env = env
        self.body = list()
        self.body.append((self.maze_env.get_start_point()[0], self.maze_env.get_start_point()[1]))

    def select_next(self) -> Tuple[int, int]:
        # choosing one of the states of the body completely randomly
        random_body = random.choice(self.body)
        # getting list of possible neighbours for the selected state
        neighbours = self.maze_env.get_neighbours(random_body[0], random_body[1])
        if len(neighbours) == 0:
            return self.select_next()
        # selecting one of the neighbours completely randomly
        random_neighbour = random.sample(neighbours, 1)
        # adding the selected neighbour to the list body
        self.body.append(random_neighbour[0])
        return random_neighbour[0][0], random_neighbour[0][1]

