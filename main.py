from stmlearn.equivalencecheckers import SmartWmethodEquivalenceChecker, Sequential
from stmlearn.equivalencecheckers.experimental import GeneticEquivalenceChecker
from stmlearn.learners import TTTMealyLearner
from stmlearn.util import MATExperiment
from stmlearn.suls import MealyDotSUL
from stmlearn.teachers import Teacher



benchmark_setups = {
    'normal': lambda sul: MATExperiment(
        learner=TTTMealyLearner,
        teacher=Teacher(
            sul=sul,
            eqc=SmartWmethodEquivalenceChecker(
                horizon=5,
                stop_on='error'
            )
        )
    ),
    'genetic': lambda sul: MATExperiment(
        learner=TTTMealyLearner,
        teacher=Teacher(
            sul=sul,
            eqc=Sequential(
                GeneticEquivalenceChecker,
                SmartWmethodEquivalenceChecker(
                    horizon=5,
                    stop_on='error'
                )
            )
        )
    )
}

problem = 'm55'

for type in benchmark_setups.keys():
    sul = MealyDotSUL(f'benchmarks/BenchmarkASMLRERS2019/{problem}.dot')
    experiment = benchmark_setups[type](sul)
    experiment.enable_logging(f'logs/{type}', problem, log_interval=10)
    hyp = experiment.run()

    print("Hyp states:", len(hyp.get_states()))
    print("Real states:", len(sul.edge_map))