import time
from collections import namedtuple
from pathlib import Path
import sys
import os
import libtmux


Job = namedtuple('Job', ['name', 'experiment_type', 'benchmark_path'])

def yesno(question):
    """Simple Yes/No Function."""
    prompt = f'{question}? (y/n): '
    ans = input(prompt).strip().lower()
    if ans not in ['y', 'n']:
        print(f'{ans} is invalid, please try again...')
        return yesno(question)
    if ans == 'y':
        return True
    return False

session_name = "benchmarks"
experiment_types = ['wmethod', 'genetic']
max_jobs = 8
max_windows = max_jobs + 1

# Collect paths
path = "benchmarks/BenchmarkASMLRERS2019"
benchmarks = list(sorted(Path("benchmarks/BenchmarkASMLRERS2019").glob("*.dot"), key=os.path.getsize))

# See if we need to start a tmux session
server = libtmux.Server()
if server.has_session(session_name):
    do_kill = yesno(f"Session {session_name} exists, kill it")
    if do_kill:
        server.kill_session(session_name)
    else:
        sys.exit()
session = server.new_session(session_name)

# Generate jobs
jobs = []
jobs_done = 0

for benchmark_path in benchmarks:
    benchmark_name = benchmark_path.stem

    for experiment_type in experiment_types:
        job = Job(
            name=f'{benchmark_name}-{experiment_type}',
            experiment_type=experiment_type,
            benchmark_path=benchmark_path
        )
        jobs.append(job)

while len(jobs) > 0:
    time.sleep(5)

    # check the tmux panes if theyre done
    for window in session.list_windows():
        pane = window.attached_pane
        pane_lines = pane.capture_pane()
        if len(pane_lines) > 1:
            if pane_lines[-2] == "DONE":
                session.kill_window(window.get('window_name'))

    n_windows = len(session.list_windows())
    if len(jobs) > 0 and n_windows < max_windows:
        job = jobs.pop(0)

        window = session.new_window(
            window_name=job.name,
            attach=False
        )
        pane = window.attached_pane
        pane.send_keys("source venv/bin/activate")
        pane.send_keys(f"python benchmark.py {job.benchmark_path} {job.experiment_type} --timeout {60 * 10} && echo DONE")

