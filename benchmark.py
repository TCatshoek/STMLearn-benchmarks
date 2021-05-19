from stmlearn.equivalencecheckers import SmartWmethodEquivalenceChecker, Sequential
from stmlearn.equivalencecheckers.experimental import GeneticEquivalenceChecker
from stmlearn.learners import TTTMealyLearner
from stmlearn.suls import MealyDotSUL
from stmlearn.util import MATExperiment, bfs, Logger
from stmlearn.suls._rerssoconnector import RERSSOConnector
from stmlearn.teachers import Teacher

from pathlib import Path

import argparse

parser = argparse.ArgumentParser(description='Run benchmark experiment')
parser.add_argument('path', type=Path)
parser.add_argument('type', type=str, choices=['wmethod', 'genetic'])
parser.add_argument('--timeout', type=int, default=60, help="Timeout in seconds")
args = parser.parse_args()


def create_wmethod(sul):
    return MATExperiment(
        learner=TTTMealyLearner,
        teacher=Teacher(
            sul=sul,
            eqc=SmartWmethodEquivalenceChecker(
                horizon=7,
                stop_on={'invalid_input'},
                stop_on_startswith={'error'}
            )
        )
    )


def create_genetic(sul):
    return MATExperiment(
        learner=TTTMealyLearner,
        teacher=Teacher(
            sul=sul,
            eqc=Sequential(
                GeneticEquivalenceChecker,
                SmartWmethodEquivalenceChecker(
                    horizon=7,
                    stop_on={'invalid_input'},
                    stop_on_startswith={'error'}
                )
            )
        )
    )


path = args.path
type = args.type
problem = path.stem
print("loading:", path)
sul = MealyDotSUL(path)

if type == 'wmethod':
    experiment = create_wmethod(sul)
elif type == 'genetic':
    experiment = create_genetic(sul)
else:
    raise Exception("Invalid type")

experiment.set_timeout(args.timeout)

# Set up the logging
experiment.enable_logging(f'logs/{type}', problem,
                          log_interval=10,
                          write_on_change={'STATE_COUNT'})
Logger().write()

# Set up the counterexample tracking for the genetic eq checker
experiment.enable_ct_tracking()
experiment.run()
Logger().write()
