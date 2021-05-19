from stmlearn.util import parse_log
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Logs are organized according to:
#   - experiment name
#       - benchmark name
#           - run time & date
def gather_data(base_path):
    experiments = {}

    for exp_dir in [x for x in Path(base_path).glob("*") if x.is_dir()]:
        experiment_name = exp_dir.stem
        experiments[experiment_name] = {}

        for bench_dir in [x for x in exp_dir.glob("*") if x.is_dir()]:
            benchmark_name = bench_dir.stem

            # Find latest run dir
            run_dirs = [x for x in bench_dir.glob("*") if x.is_dir()]
            latest_run_dir = sorted(run_dirs, key=lambda x: x.stem)[0]

            # Read and parse the log
            log_path = latest_run_dir.joinpath("log.txt")
            df = pd.DataFrame.from_dict(data=parse_log(log_path)) \
                .astype({
                'Log.MEMBERSHIP': int,
                'Log.EQUIVALENCE': int,
                'Log.TEST': int,
                'Log.STATE_COUNT': int
            })

            experiments[experiment_name][benchmark_name] = df

    return experiments



log_data = gather_data('logs')

# Figure out which experiments have data available in all settings
bench_names = []
for exp_type in log_data.keys():
     bnames = log_data[exp_type].keys()
     bench_names.append(set(bnames))
benchmarks_ran = set.intersection(*bench_names)

# Ensure plots dir exists
Path("plots").mkdir(exist_ok=True)

# Create comparison plots
exp_names = log_data.keys()
for benchmark in benchmarks_ran:
    for exp_name in exp_names:
        df = log_data[exp_name][benchmark]
        plt.plot(df['timestamp'], df['Log.STATE_COUNT'], label=exp_name)
    plt.legend()
    plt.savefig(f'plots/{benchmark}.png')
    plt.close()



