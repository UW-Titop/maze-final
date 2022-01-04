import math

from benchmark.QLearningBenchmark import QLearningBenchmark
from env.DepthFirstMazeEnv import DepthFirstMazeEnv
from env.KruskalMazeEnv import KruskalMazeEnv


if __name__ == '__main__':

    env_list = list()
    env_list.append(DepthFirstMazeEnv())
    env_list.append(KruskalMazeEnv())


    try_per_size = 100
    minimum_env_size = 16
    maximum_env_size = 16

    size_list = list()
    size_list.append((minimum_env_size, minimum_env_size))
    for i in range(int(math.log(minimum_env_size, 2)), int(math.log(maximum_env_size, 2))):
        size_list.append((size_list[-1][0] * 2, size_list[-1][1] * 2))
    env_size_list = list()
    for size in size_list:
        env_size_list.append(size)
    QLearningBenchmark(env_list, env_size_list, try_per_size, 1000)

