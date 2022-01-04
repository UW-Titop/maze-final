import sys


from env.DepthFirstMazeEnv import DepthFirstMazeEnv
from solver.AStarMazeSolver import AStarMazeSolver
from solver.BestFirstMazeSolver import BestFirstMazeSolver
from solver.BodyRandomMazeSolver import BodyRandomMazeSolver
from solver.BreadthFirstMazeSolver import BreadthFirstMazeSolver
from solver.HeadRandomMazeSolver import HeadRandomMazeSolver
from solver.WallFollowerMazeSolver import WallFollowerMazeSolver
from solver.QLearningMazeSolver import QLearningMazeSolver
from env.KruskalMazeEnv import KruskalMazeEnv
from interface.PygameInterface import PygameInterface


if __name__ == '__main__':
    # env = DepthFirstMazeEnv()
    env = KruskalMazeEnv()
    env.init(64, 64)

    # solver = BreadthFirstMazeSolver()
    solver = WallFollowerMazeSolver()
    # solver = AStarMazeSolver()
    # solver = QLearningMazeSolver(500)
    # solver = BodyRandomMazeSolver()
    # solver = HeadRandomMazeSolver()
    solver.init(env)
    pygame_output = PygameInterface(env, solver)
    pygame_output.animate()
