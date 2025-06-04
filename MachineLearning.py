import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

def graphRawFX():
    date, bid, ask = np.loadtxt('testDate/GBPUSD/GBPUSD1d.txt', unpack=True, delimiter=',', converters={0: custom_date_converter})
    fig = plt.figure(figsize=(10, 7))
    ax1 = plt.subplot2grid((40, 40), (0, 0), rowspan=40, colspan=40)

    ax1.plot(date, bid)
    ax1.plot(date, ask)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    plt.grid(True)
    plt.show()

def custom_date_converter(s):
    return mdates.date2num(datetime.strptime(s.decode('utf-8'), '%Y%m%d%H%M%S'))
