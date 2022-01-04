from benchmark.SolverBenchmark import SolverBenchmark
from env.DepthFirstMazeEnv import DepthFirstMazeEnv
from solver.AStarMazeSolver import AStarMazeSolver
from solver.BestFirstMazeSolver import BestFirstMazeSolver
from solver.BodyRandomMazeSolver import BodyRandomMazeSolver
from solver.HeadRandomMazeSolver import HeadRandomMazeSolver
from solver.WallFollowerMazeSolver import WallFollowerMazeSolver
from env.KruskalMazeEnv import KruskalMazeEnv

import threading


class MyThread(threading.Thread):

    def __init__(self, env_list: list, solver_list: list, env_size_list: list, id: int):
        threading.Thread.__init__(self)
        self.env_list = env_list
        self.solver_list = solver_list
        self.env_size_list = env_size_list
        self.id = id

    def run(self) -> None:
        SolverBenchmark(self.env_list, self.solver_list, 40, self.env_size_list) \
            .get_metadata() \
            .to_csv('output' + str(self.id) + '.csv')


if __name__ == '__main__':
    env_list_1 = list()
    env_1 = DepthFirstMazeEnv()
    env_list_1.append(env_1)
    env_1 = KruskalMazeEnv()
    env_list_1.append(env_1)

    solver_list_1 = list()
    solver_list_1.append(AStarMazeSolver())
    solver_list_1.append(BestFirstMazeSolver())
    solver_list_1.append(BodyRandomMazeSolver())
    solver_list_1.append(HeadRandomMazeSolver())
    solver_list_1.append(WallFollowerMazeSolver())

    env_size_list_1 = list()
    env_size_list_1.append((8, 8))
    env_size_list_1.append((16, 16))
    env_size_list_1.append((32, 32))
    thread_1 = MyThread(env_list_1, solver_list_1, env_size_list_1, 1)
    thread_1.start()

    ########
    env_list_2 = list()
    env_2 = DepthFirstMazeEnv()
    env_list_2.append(env_2)
    env_2 = KruskalMazeEnv()
    env_list_2.append(env_2)


    solver_list_2 = list()
    solver_list_2.append(AStarMazeSolver())
    solver_list_2.append(BestFirstMazeSolver())
    solver_list_2.append(BodyRandomMazeSolver())
    solver_list_2.append(HeadRandomMazeSolver())
    solver_list_2.append(WallFollowerMazeSolver())

    env_size_list_2 = list()
    env_size_list_2.append((64, 64))
    thread_2 = MyThread(env_list_2, solver_list_2, env_size_list_2, 2)
    thread_2.start()
    ##############

    ########
    env_list_3 = list()
    env_3 = DepthFirstMazeEnv()
    env_list_3.append(env_3)
    env_3 = KruskalMazeEnv()
    env_list_3.append(env_3)

    solver_list_3 = list()
    solver_list_3.append(AStarMazeSolver())
    solver_list_3.append(BestFirstMazeSolver())
    solver_list_3.append(BodyRandomMazeSolver())
    solver_list_3.append(HeadRandomMazeSolver())
    solver_list_3.append(WallFollowerMazeSolver())

    env_size_list_3 = list()
    env_size_list_3.append((64, 64))
    thread_3 = MyThread(env_list_3, solver_list_3, env_size_list_3, 3)
    thread_3.start()
    ##############

    ########
    env_list_4 = list()
    env_4 = DepthFirstMazeEnv()
    env_list_4.append(env_4)
    env_4 = KruskalMazeEnv()
    env_list_4.append(env_4)

    solver_list_4 = list()
    solver_list_4.append(AStarMazeSolver())
    solver_list_4.append(BestFirstMazeSolver())
    solver_list_4.append(BodyRandomMazeSolver())
    solver_list_4.append(HeadRandomMazeSolver())
    solver_list_4.append(WallFollowerMazeSolver())

    env_size_list_4 = list()
    env_size_list_4.append((128, 128))
    thread_4 = MyThread(env_list_4, solver_list_4, env_size_list_4, 4)
    thread_4.start()
    ##############

    print("waiting for thread_1 ...")
    thread_1.join()
    print("waiting for thread_2 ...")
    thread_2.join()
    print("waiting for thread_3 ...")
    thread_3.join()
    print("waiting for thread_4 ...")
    thread_4.join()
    print("finished")



