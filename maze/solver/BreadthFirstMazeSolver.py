from typing import Tuple

from solver.MazeSolver import MazeSolver
from env.MazeEnv import MazeEnv


class BreadthFirstMazeSolver(MazeSolver):

    # storing list of all steps
    queue = None

    def init(self, env: MazeEnv):
        self.maze_env = env
        self.queue = list()
        self.queue.append((self.maze_env.get_start_point()[0], self.maze_env.get_start_point()[1]))

    def select_next(self) -> Tuple[int, int]:
        # the future action should be selected according to the first item in the list
        current_row = self.queue[0][0]
        current_col = self.queue[0][1]
        neighbours = self.maze_env.get_neighbours(current_row, current_col)
        # we need at least a state with neighbours
        while len(neighbours) == 0:
            # if the selected state does not have neighbour, we must delete it and select the next state in the queue
            del self.queue[0]
            current_row = self.queue[0][0]
            current_col = self.queue[0][1]
            neighbours = self.maze_env.get_neighbours(current_row, current_col)
        # the selected neighbour must be added to the end of the list
        self.queue.append(neighbours[0])
        return neighbours[0][0], neighbours[0][1]

