import time
from pandas import DataFrame
from pympler import asizeof


class EnvBenchmark:
    # this dataframe is used to store all the information
    dataframe = DataFrame()

    def __init__(self, env_list: list, try_per_env: int, env_size_list: list):
        for i in range(try_per_env):
            for env in env_list:
                for width, height in env_size_list:
                    env_before = time.time_ns()
                    env.init(width, height)
                    env_after = time.time_ns()
                    my_dict = {
                        # we store the time that took to generate the environment
                        "env_generation_time": env_after - env_before,
                        # we store the total memory that generating the environment used
                        "env_used_memory": asizeof.asizeof(env),
                        # we store the width of the environment
                        "env_width": width,
                        # we store the height of the environment
                        "env_height": height,
                        # we store the name of the algorithm that is used to generate the env
                        "env_algorithm": type(env).__name__
                    }
                    self.dataframe = self.dataframe.append(my_dict, ignore_index=True)

    def get_metadata(self):
        return self.dataframe
