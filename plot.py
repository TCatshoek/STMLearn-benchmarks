from stmlearn.util import parse_log
import pandas as pd
import matplotlib.pyplot as plt

path = "/home/tom/projects/STMLearn-benchmarks/logs/m55/2021-04-29_14:11:21/log.txt"
df = pd.DataFrame.from_dict(data=parse_log(path)) \
    .astype({'Log.MEMBERSHIP': int, 'Log.EQUIVALENCE': int, 'Log.TEST': int})

plt.plot(df['timestamp'], df['Log.MEMBERSHIP'], color='blue')
plt.plot(df['timestamp'], df['Log.TEST'], color='red')
plt.show()
