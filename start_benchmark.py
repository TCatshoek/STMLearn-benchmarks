from pathlib import Path
import sys
import libtmux

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

# Collect paths
path = "rers/TrainingSeqReachRers2019"
benchmarks = [x for x in (sorted(Path(path).glob("*"))) if x.is_dir()]

# See if we need to start a tmux session
server = libtmux.Server()
if server.has_session(session_name):
    do_kill = yesno(f"Session {session_name} exists, kill it")
    if do_kill:
        server.kill_session(session_name)
    else:
        sys.exit()
session = server.new_session(session_name)

for benchmark_path in benchmarks:
    benchmark_name = benchmark_path.stem

    for experiment_type in experiment_types:
        window = session.new_window(
            window_name=f'{benchmark_name}-{experiment_type}',
            attach=False
        )
        pane = window.attached_pane
        pane.send_keys("source venv/bin/activate")
        pane.send_keys(f"python rers.py {benchmark_path} {experiment_type} --timeout {60 * 10} && echo DONE")

