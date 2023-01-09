import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd
import math

var = pd.read_excel("Onedaypackets.xlsx")

y = list(var['Minuit'].fillna(0))
x = list(var['Minutes'])
# plt.figure()
# plt.plot(x,y)
# plt.xlabel('Minutes')
# plt.ylabel('Number of packets')
# plt.title('Number of packets by minutes of a day')
# plt.show()

# only care about the presence of events, not the number of packets
y_unit = [math.sqrt(i) for i in y]   # attenuate the large numbers

f, Pxx_den = signal.periodogram(y_unit,1/60)

# remove low frequencies (events happening with more than 1h in between, need longer data if still wanted)
no_low = f > 1/3600
f = f[no_low]
Pxx_den = Pxx_den[no_low]

plt.figure()
plt.plot(f, Pxx_den)  # no logscale needed
plt.xlabel('Frequency [Hz]')
plt.ylabel('Spectrum')
plt.title('Periodigram from a day worth of data')
plt.show()

# find spikes in frequencies
max_P = max(Pxx_den)
threshold = Pxx_den > (max_P * 0.8)  # you can play with the threshold
print('Found events happening every', 1 / f[threshold], 'seconds.')
