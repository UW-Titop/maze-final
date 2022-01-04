import copy
import time
import uuid
from pandas import DataFrame
from pympler import asizeof


class SolverBenchmark:
    # this dataframe is used to store all the information
    dataframe = DataFrame()

    def __init__(self, env_list: list, solver_list: list, epochs: int, env_size_list: list):
        for env in env_list:
            for width, height in env_size_list:

                env_before = time.time_ns()
                env.init(width, height)
                env_after = time.time_ns()

                env_hex = uuid.uuid4().hex
                for solver in solver_list:
                    my_dict = {
                        # Storing an UUID that will be generated for each environment
                        "env_hex": env_hex,
                        # Storing the time that took to generate the environment
                        "env_generation_time": env_after - env_before,
                        # Storing the total memory that generating the environment used
                        "env_used_memory": asizeof.asizeof(env),
                        # Storing the width of the environment
                        "env_width": width,
                        # Storing the height of the environment
                        "env_height": height,
                        # Storing the name of the algorithm that is used to generate the env
                        "env_algorithm": type(env).__name__,
                        # Storing the name of the algorithm that is used to solve the environment
                        "solver_algorithm": type(solver).__name__
                    }
                    for epoch in range(epochs):
                        temp_env = copy.deepcopy(env)
                        temp_solver = copy.deepcopy(solver)
                        temp_solver.init(temp_env)
                        counter = 0
                        now = time.time_ns()
                        while not temp_solver.get_finished():
                            temp_solver.tick()
                            counter += 1
                        # Epoch is mainly used for algorithms that work randomly
                        my_dict["solver_epoch"] = epoch
                        # Number of total steps that the agent took to solve the algorithm
                        my_dict["solver_steps"] = counter
                        # Total time that took to solve the environment by agent
                        my_dict["solver_time"] = time.time_ns() - now
                        # Storing the memory that the solver used to solve the environment
                        my_dict["solver_used_memory"] = asizeof.asizeof(temp_solver)
                        # Storing a boolean variable to make sure that the environment is solved successfully or not
                        my_dict["successful"] = temp_solver.get_successful()
                        self.dataframe = self.dataframe.append(my_dict, ignore_index=True)
                # Writing the dataframe to disk for persistence
                self.write(str(time.time_ns()))

    def get_metadata(self) -> DataFrame:
        return self.dataframe

    def write(self, name: str) -> None:
        self.get_metadata().to_csv('output-' + name + '.csv')
