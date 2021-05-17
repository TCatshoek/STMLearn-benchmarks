from stmlearn.util import parse_log
import pandas as pd
import matplotlib.pyplot as plt

path_1 = "/home/tom/projects/STMLearn-benchmarks/logs/genetic/m54/2021-05-17_19:28:25/log.txt"
df_1 = pd.DataFrame.from_dict(data=parse_log(path_1)) \
    .astype({'Log.MEMBERSHIP': int, 'Log.EQUIVALENCE': int, 'Log.TEST': int, 'Log.STATE_COUNT': int})

path_2 = "/home/tom/projects/STMLearn-benchmarks/logs/normal/m54/2021-05-17_19:28:07/log.txt"
df_2 = pd.DataFrame.from_dict(data=parse_log(path_2)) \
    .astype({'Log.MEMBERSHIP': int, 'Log.EQUIVALENCE': int, 'Log.TEST': int, 'Log.STATE_COUNT': int})

plt.plot(df_1['timestamp'], df_1['Log.STATE_COUNT'], color='blue', label='genetic')
plt.plot(df_2['timestamp'], df_2['Log.STATE_COUNT'], color='red', label='wmethod')
plt.legend()
plt.show()
