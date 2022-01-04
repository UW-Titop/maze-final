import random
from typing import Tuple

from solver.MazeSolver import MazeSolver
from env.MazeEnv import MazeEnv


class WallFollowerMazeSolver(MazeSolver):

    # storing all steps
    path_stack = None

    def init(self, maze_env: MazeEnv):
        starting_point = maze_env.get_start_point()
        self.maze_env = maze_env
        self.path_stack = list()
        self.path_stack.append(starting_point)

    def get_top(self):
        return self.path_stack[-1]

    def get_second_top(self):
        return self.path_stack[-2]

    def tick(self) -> Tuple[int, int]:
        top = self.get_top()
        neighbours = self.maze_env.get_neighbours_custom(top[0], top[1])
        # for the first step, the direction is not known. We must handle it differently.
        if len(self.path_stack) < 2:
            next = self.handle_first_move(neighbours)
        else:
            # The agent must keep its direction.
            # If it is going right, it must not return unless it reaches to a dead end.
            second_top = self.get_second_top()
            if len(neighbours) == 0:
                self.path_stack.append(second_top)
                next = second_top[0], second_top[1]
            elif self.is_going_down():
                next = self.handle_going_down(neighbours)
            elif self.is_going_left():
                next = self.handle_going_left(neighbours)
            elif self.is_going_up():
                next = self.handle_going_up(neighbours)
            elif self.is_going_right():
                next = self.handle_going_right(neighbours)
            else:
                print(top)
                print(second_top)
                raise ValueError('Error!')
        # there are some situations that the Wall Follower algorithm cannot handle.
        # In these situations, we select the next action randomly.
        # This happens rarely, if we do not put this code, the algorithm hangs forever without making any progress
        if self.path_stack.count(next) > 2:
            next = random.choice(neighbours)
        self.path_stack.append(next)
        self.maze_env.fill(next[0], next[1])

        finish_row, finish_col = self.maze_env.get_finish_point()
        if next[0] == finish_row and next[1] == finish_col:
            self.finish_and_successful()
        return next[0], next[1]

    # checking that the down is a valid neighbour or not
    def down_is_available(self, neighbours: list) -> bool:
        for neighbour in neighbours:
            if neighbour[1] > self.get_top()[1]:
                return True
        return False

    # checking that the up is a valid neighbour or not
    def up_is_available(self, neighbours: list) -> bool:
        for neighbour in neighbours:
            if neighbour[1] < self.get_top()[1]:
                return True
        return False

    # checking that the left is a valid neighbour or not
    def left_is_available(self, neighbours: list) -> bool:
        for neighbour in neighbours:
            if neighbour[0] < self.get_top()[0]:
                return True
        return False

    # checking that the right is a valid neighbour or not
    def right_is_available(self, neighbours: list) -> bool:
        for neighbour in neighbours:
            if neighbour[0] > self.get_top()[0]:
                return True
        return False

    # this function detect the direction of the agent according to its last two actions
    def detect_direction(self):
        top_row = self.get_top()[0]
        top_col = self.get_top()[1]
        second_top_row = self.get_second_top()[0]
        second_top_col = self.get_second_top()[1]
        return second_top_row - top_row, second_top_col - top_col

    def is_going_down(self):
        row, col = self.detect_direction()
        return row == 0 and col == -1

    def is_going_up(self):
        row, col = self.detect_direction()
        return row == 0 and col == 1

    def is_going_left(self):
        row, col = self.detect_direction()
        return row == 1 and col == 0

    def is_going_right(self):
        row, col = self.detect_direction()
        return row == -1 and col == 0

    # selecting the next action if the agent is going up
    def handle_going_up(self, neighbours):
        if self.right_is_available(neighbours):
            return self.go_right()
        elif self.up_is_available(neighbours):
            return self.go_up()
        elif self.left_is_available(neighbours):
            return self.go_left()
        else:
            return self.go_down()

    # selecting the next action if the agent is going left
    def handle_going_left(self, neighbours):
        if self.up_is_available(neighbours):
            return self.go_up()
        elif self.left_is_available(neighbours):
            return self.go_left()
        elif self.down_is_available(neighbours):
            return self.go_down()
        else:
            return self.go_right()

    # selecting the next action if the agent is going down
    def handle_going_down(self, neighbours):
        if self.left_is_available(neighbours):
            return self.go_left()
        elif self.down_is_available(neighbours):
            return self.go_down()
        elif self.right_is_available(neighbours):
            return self.go_right()
        else:
            return self.go_up()

    # selecting the next action if the agent is going right
    def handle_going_right(self, neighbours: list):
        if self.down_is_available(neighbours):
            return self.go_down()
        elif self.right_is_available(neighbours):
            return self.go_right()
        elif self.up_is_available(neighbours):
            return self.go_up()
        else:
            return self.go_left()

    def handle_first_move(self, neighbours):
        if self.right_is_available(neighbours):
            return self.go_right()
        elif self.up_is_available(neighbours):
            return self.go_up()
        elif self.left_is_available(neighbours):
            return self.go_left()
        elif self.down_is_available(neighbours):
            return self.go_down()
        else:
            raise ValueError('Error!')

    def go_left(self):
        return self.get_top()[0] - 1, self.get_top()[1]

    def go_right(self):
        return self.get_top()[0] + 1, self.get_top()[1]

    def go_up(self):
        return self.get_top()[0], self.get_top()[1] - 1

    def go_down(self):
        return self.get_top()[0], self.get_top()[1] + 1
