
import os
import pandas
import re

import matplotlib.pyplot as plt
from matplotlib import use,rcParams

# latex settings
#use("pgf")
#rcParams.update({
#    "pgf.texsystem": "pdflatex",
#    'font.family': 'serif',
#    'text.usetex': True,
#    'pgf.rcfonts': False,
#})

# metrics ->  user -> devices 

def load_all_csv(metrics_path, expression=".*.csv", **kwargs) -> pandas.Series :
    regexp = re.compile(expression)
    filename_list = []
    df_list = []
    for root, subdirs, files in os.walk(metrics_path, followlinks=True):
        file_list = list(filter(regexp.match, files))
        for filename in file_list:
            filename_list.append(filename)
            df_list.append(
                pandas.read_csv(
                    os.path.join(root, filename),
                    **kwargs,delimiter=";")
                    
                )

    if df_list:
        df = pandas.concat(df_list)
    else:
        df = pandas.Series()
    return df

df= load_all_csv("/usr/src/app/metrics/devices")
len(df)
fig1, ax1 = plt.subplots()
#ax1.set_title('Duration')
#ax1.boxplot(df['DURATION'])
ax1.boxplot(df['DURATION'],labels=["DURATION"])
plt.savefig('duration.png')


#plt.savefig('duration.pgf')