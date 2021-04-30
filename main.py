from stmlearn.equivalencecheckers import WmethodEquivalenceChecker
from stmlearn.equivalencecheckers import SmartWmethodEquivalenceChecker
from stmlearn.learners import TTTMealyLearner
from stmlearn.util import MATExperiment
from stmlearn.suls import MealyDotSUL
from stmlearn.teachers import Teacher

problem = 'm55'
sul = MealyDotSUL(f'benchmarks/BenchmarkASMLRERS2019/{problem}.dot')

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
    )
}

print(sul.get_alphabet())
experiment = benchmark_setups['normal'](sul)
#experiment.set_timeout(10)
experiment.enable_logging('logs', problem, log_interval=1)
hyp = experiment.run()

print("Hyp states:", len(hyp.get_states()))
print("Real states:", len(sul.edge_map))