from benchmark.EnvBenchmark import EnvBenchmark
from env.DepthFirstMazeEnv import DepthFirstMazeEnv
from env.KruskalMazeEnv import KruskalMazeEnv

if __name__ == '__main__':

    env_list = list()
    env_list.append(DepthFirstMazeEnv())
    env_list.append(KruskalMazeEnv())

    env_size_list = list()
    env_size_list.append((8, 8))
    env_size_list.append((16, 16))
    env_size_list.append((32, 32))
    env_size_list.append((64, 64))
    env_size_list.append((128, 128))
    # env_size_list.append((256, 256))
    # env_size_list.append((512, 512))

    EnvBenchmark(env_list, 1, env_size_list).get_metadata().to_csv('env-benchmark' + str(9999) + '.csv')
