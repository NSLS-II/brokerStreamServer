
from channelarchiver import codes, Archiver
import matplotlib.pyplot as plt
import re




def plot(archiver, xchannel, ychannel, start, end):
    x,y = archiver.get([xchannel, ychannel], start, end, interpolation=codes.interpolation.RAW)
    xvalues = [None] * x.times.__len__()
    yvalues = [None] * x.times.__len__()
    for date in x.times :
        if y.times.index(date) is not None :
            xvalues[x.times.index(date)] =  x.values[x.times.index(date)]
            yvalues[x.times.index(date)] = y.values[y.times.index(date)]
    plt.ylabel(x.channel)
    plt.xlabel(y.channel)
    plt.plot(xvalues, yvalues)
    plt.show()