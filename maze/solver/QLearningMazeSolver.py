import copy
import time
from typing import Tuple

import numpy as np

from env.MazeEnv import MazeEnv
from solver.MazeSolver import MazeSolver


class QLearningMazeSolver(MazeSolver):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

    number_of_actions = 4
    number_of_episodes = 100
    episode_counter = 0
    q_table = np.ndarray
    head_row = None
    head_col = None

    original_maze_env = MazeEnv()

    benchmark_dict = None
    episode_start_time = None
    episode_total_reward = None

    def __init__(self, number_of_episodes):
        self.number_of_episodes = number_of_episodes

    def init(self, maze_env: MazeEnv):
        self.maze_env = maze_env
        self.original_maze_env = copy.deepcopy(maze_env)
        self.init_q_table(maze_env)
        self.head_row, self.head_col = maze_env.get_start_point()
        self.episode_start_time = time.time_ns()
        self.episode_counter = 0
        self.benchmark_dict = dict()
        self.episode_total_reward = 0

    def init_q_table(self, maze_env: MazeEnv):
        # the initial value of the q-table is zero
        self.q_table = np.zeros((
            maze_env.get_row_size(), maze_env.get_col_size(), self.number_of_actions))

    def tick(self) -> Tuple[int, int]:
        neighbours = self.maze_env.get_neighbours(self.head_row, self.head_col)
        if len(neighbours) < 1:
            # we store the information of each episode for benchmarking process
            self.benchmark_dict[f"episode-{self.episode_counter}-start-timestamp"] = self.episode_start_time
            self.benchmark_dict[f"episode-{self.episode_counter}-finish-timestamp"] = time.time_ns()
            self.benchmark_dict[f"episode-{self.episode_counter}-duration"] = time.time_ns() - self.episode_start_time
            self.benchmark_dict[f"episode-{self.episode_counter}-successful"] = '0'
            self.benchmark_dict[f"episode-{self.episode_counter}-reward"] = self.episode_total_reward
            self.episode_counter += 1
            if self.episode_counter > self.number_of_episodes:
                # if number of taken episodes exceeds the limitation, we have to end the process
                self.finish_and_unsuccessful()
            else:
                # if agent goes to a state without any neighbour, it must receive a big negative reward.
                # q-table will be updated according to the reward
                punishment_reward = -50
                self.q_table[self.head_row, self.head_col, self.UP] = punishment_reward
                self.q_table[self.head_row, self.head_col, self.DOWN] = punishment_reward
                self.q_table[self.head_row, self.head_col, self.LEFT] = punishment_reward
                self.q_table[self.head_row, self.head_col, self.RIGHT] = punishment_reward
                self.episode_total_reward += punishment_reward

                self.maze_env = copy.deepcopy(self.original_maze_env)
                self.do_reset()
                self.head_row, self.head_col = self.maze_env.get_start_point()
            return self.maze_env.get_start_point()

        # to select the next state, we need to understand the direction of current state to the neighbour.
        # It is required for selecting the neighbour with the highest reward.
        direction_row, direction_col = self.detect_direction(self.head_row, self.head_col,
                                                             neighbours[0][0], neighbours[0][1])
        best_row, best_col = neighbours[0][0], neighbours[0][1]
        best_value = self.get_value(direction_row, direction_col)

        # the best neighbour is the neighbour with the highest reward
        for neighbour in neighbours[1:]:
            current_direction_row, current_direction_col = self.detect_direction(self.head_row, self.head_col,
                                                                                 neighbour[0], neighbour[1])
            current_value = self.get_value(current_direction_row, current_direction_col)

            current_row, current_col = neighbour[0], neighbour[1]
            if current_value > best_value:
                best_value = current_value
                best_row, best_col = current_row, current_col

        self.maze_env.fill(best_row, best_col)

        direction_row, direction_col = self.detect_direction(self.head_row, self.head_col, best_row, best_col)
        action_reward = self.get_avg(best_row, best_col)
        self.episode_total_reward += action_reward

        # each action has a reward. Q-table must be updated according to the action.
        if self.is_going_up(direction_row, direction_col):
            self.q_table[self.head_row, self.head_col, self.UP] += action_reward
        elif self.is_going_down(direction_row, direction_col):
            self.q_table[self.head_row, self.head_col, self.DOWN] += action_reward
        elif self.is_going_left(direction_row, direction_col):
            self.q_table[self.head_row, self.head_col, self.LEFT] += action_reward
        elif self.is_going_right(direction_row, direction_col):
            self.q_table[self.head_row, self.head_col, self.RIGHT] += action_reward

        finish_row, finish_col = self.maze_env.get_finish_point()
        if best_row == finish_row and best_col == finish_col:
            # we store the information of each episode for benchmarking process
            self.benchmark_dict[f"episode-{self.episode_counter}-start-timestamp"] = self.episode_start_time
            self.benchmark_dict[f"episode-{self.episode_counter}-finish-timestamp"] = time.time_ns()
            self.benchmark_dict[f"episode-{self.episode_counter}-duration"] = time.time_ns() - self.episode_start_time
            self.benchmark_dict[f"episode-{self.episode_counter}-successful"] = '1'
            self.benchmark_dict[f"episode-{self.episode_counter}-reward"] = self.episode_total_reward
            self.episode_counter += 1
            if self.episode_counter > self.number_of_episodes:
                self.finish_and_successful()
            else:
                # if agent goes to goal state, it must receive a big positive reward.
                # q-table will be updated according to the reward
                direction_row, direction_col = self.detect_direction(self.head_row, self.head_col, best_row, best_col)
                congrats_reward = 100
                if self.is_going_up(direction_row, direction_col):
                    self.q_table[self.head_row, self.head_col, self.UP] += congrats_reward
                elif self.is_going_down(direction_row, direction_col):
                    self.q_table[self.head_row, self.head_col, self.DOWN] += congrats_reward
                elif self.is_going_left(direction_row, direction_col):
                    self.q_table[self.head_row, self.head_col, self.LEFT] += congrats_reward
                elif self.is_going_right(direction_row, direction_col):
                    self.q_table[self.head_row, self.head_col, self.RIGHT] += congrats_reward

                self.maze_env = copy.deepcopy(self.original_maze_env)
                self.do_reset()
                self.head_row, self.head_col = self.maze_env.get_start_point()
                self.episode_start_time = time.time_ns()
            return self.maze_env.get_start_point()

        self.head_row = best_row
        self.head_col = best_col
        return best_row, best_col

    # this function returns the value of going to the neighbour from current state
    def get_value(self, current_direction_row, current_direction_col):
        if self.is_going_up(current_direction_row, current_direction_col):
            return self.q_table[self.head_row, self.head_col, self.UP]
        elif self.is_going_down(current_direction_row, current_direction_col):
            return self.q_table[self.head_row, self.head_col, self.DOWN]
        elif self.is_going_left(current_direction_row, current_direction_col):
            return self.q_table[self.head_row, self.head_col, self.LEFT]
        elif self.is_going_right(current_direction_row, current_direction_col):
            return self.q_table[self.head_row, self.head_col, self.RIGHT]
        else:
            raise ValueError('Error!')

    # this function returns the average value of all 4 different actions
    def get_avg(self, best_row, best_col):
        return (self.q_table[best_row, best_col, self.UP] +
         self.q_table[best_row, best_col, self.DOWN] +
         self.q_table[best_row, best_col, self.LEFT] +
         self.q_table[best_row, best_col, self.RIGHT]) / 4

    def detect_direction(self, current_row, current_col, next_row, next_col):
        return next_row - current_row, next_col - current_col

    def is_going_down(self, direction_row, direction_col):
        return direction_row == 0 and direction_col == -1

    def is_going_up(self, direction_row, direction_col):
        return direction_row == 0 and direction_col == 1

    def is_going_left(self, direction_row, direction_col):
        return direction_row == 1 and direction_col == 0

    def is_going_right(self, direction_row, direction_col):
        return direction_row == -1 and direction_col == 0

    def get_benchmark(self) -> dict:
        return self.benchmark_dict
