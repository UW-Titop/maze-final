import math


from benchmark.SolverBenchmark import SolverBenchmark
from env.DepthFirstMazeEnv import DepthFirstMazeEnv
from env.KruskalMazeEnv import KruskalMazeEnv
from solver.AStarMazeSolver import AStarMazeSolver
from solver.BestFirstMazeSolver import BestFirstMazeSolver
from solver.BodyRandomMazeSolver import BodyRandomMazeSolver
from solver.BreadthFirstMazeSolver import BreadthFirstMazeSolver
from solver.HeadRandomMazeSolver import HeadRandomMazeSolver
from solver.WallFollowerMazeSolver import WallFollowerMazeSolver


if __name__ == '__main__':

    env_list = list()
    env_list.append(DepthFirstMazeEnv())
    env_list.append(KruskalMazeEnv())

    solver_list = list()
    solver_list.append(BreadthFirstMazeSolver())
    solver_list.append(AStarMazeSolver())
    solver_list.append(BestFirstMazeSolver())
    solver_list.append(BodyRandomMazeSolver())
    solver_list.append(HeadRandomMazeSolver())
    solver_list.append(WallFollowerMazeSolver())

    try_per_size = 10
    minimum_env_size = 8
    maximum_env_size = 128
    size_list = list()
    size_list.append((minimum_env_size, minimum_env_size))
    for i in range(int(math.log(minimum_env_size, 2)), int(math.log(maximum_env_size, 2))):
        size_list.append((size_list[-1][0] * 2, size_list[-1][1] * 2))
    env_size_list = list()
    for size in size_list:
        for i in range(try_per_size):
            env_size_list.append(size)

    SolverBenchmark(env_list, solver_list, 5, env_size_list)
