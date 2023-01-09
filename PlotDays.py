import pandas as pd
import matplotlib.pyplot as plt

var = pd.read_excel("packetmin.xlsx")

y = list(var['PBisJ1'])
x = list(var['Jour1Min'])
y2 = list(var['PBisJ2'])
y3=list(var['PBisJ3'])
#y4=list(var['PBisJ4'])
#y5=list(var['PBisJ5'])

fig, axes = plt.subplots(3, 1, figsize=(12,13))
fig.suptitle('Comparing packets captured over a period of 3 days')
fig.supxlabel('Minutes')
fig.supylabel('Number of Packets')


axes[0].plot(x,y, 'tab:pink')
axes[0].set_title('Day1')

axes[1].plot(x,y2, 'tab:blue')
axes[1].set_title('Day2')

axes[2].plot(x,y3, 'tab:green')
axes[2].set_title('Day3')

#axes[3].plot(x,y4, 'tab:orange')
#axes[3].set_title('Day4')

#axes[4].plot(x,y5, 'tab:red')
#axes[4].set_title('Day5')

fig.tight_layout()

plt.show()