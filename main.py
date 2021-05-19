from stmlearn.equivalencecheckers import SmartWmethodEquivalenceChecker, Sequential
from stmlearn.equivalencecheckers.experimental import GeneticEquivalenceChecker
from stmlearn.learners import TTTMealyLearner
from stmlearn.util import MATExperiment, bfs, Logger
from stmlearn.suls import MealyDotSUL
from stmlearn.teachers import Teacher

from multiprocessing import Pool
from pathlib import Path
import os



def run_experiment(benchmark_path):
    benchmark_setups = {
        # 'normal': lambda sul: MATExperiment(
        #     learner=TTTMealyLearner,
        #     teacher=Teacher(
        #         sul=sul,
        #         eqc=SmartWmethodEquivalenceChecker(
        #             horizon=5,
        #             stop_on='error'
        #         )
        #     )
        # ),
        'genetic': lambda sul: MATExperiment(
            learner=TTTMealyLearner,
            teacher=Teacher(
                sul=sul,
                eqc=Sequential(
                    GeneticEquivalenceChecker,
                    SmartWmethodEquivalenceChecker(
                        horizon=5,
                        stop_on={'invalid_input'},
                        stop_on_startswith={'error'}
                    )
                )
            )
        )
    }

    path = benchmark_path
    problem = path.stem
    print("loading:", path)
    sul = MealyDotSUL(path)
    n_states = len(sul._get_node_names())
    print(n_states, "states")

    for type in benchmark_setups.keys():
        experiment = benchmark_setups[type](sul)
        experiment.set_timeout(60)

        # Set up the logging
        experiment.enable_logging(f'logs/{type}', problem,
                                  log_interval=10,
                                  write_on_change={'STATE_COUNT'})
        Logger().write()

        # Set up the counterexample tracking for the genetic eq checker
        experiment.enable_ct_tracking()

        experiment.run()
        Logger().write()


with Pool(1) as p:
    p.map(run_experiment, list(sorted(Path("benchmarks/BenchmarkASMLRERS2019").glob("*.dot"), key=os.path.getsize))[3:4])