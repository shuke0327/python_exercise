# these codes are derived from the qstk-tutorial3
# modules
import matplotlib.pyplot as plt
from pylab import *
from qstkutil import DataAccess as da
from qstkutil import qsdateutil as du
from qstkutil import tsutil as tsu
import datetime as dt
import numpy    as nu
 
filepath='/home/shuke0327/QSTK/Examples/Basic/tutorial3portfolio.csv'

portfolio = nu.loadtxt(filepath,dtype='S5,f4',
			delimiter=',',
			comments ='#',
			skiprows = 1,
			)

portfolio = sorted(portfolio,key=lambda x: x[0])


#param: portsyms:  contains the symbols.
#param: portalloc: contains the allocation ratio.
portsyms  = []
portalloc = []
for i in portfolio:                                #portfolio is a list object
	portsyms.append(i[0])
	portalloc.append(i[1])

# readin symbol data

dataobj       = da.DataAccess('Yahoo')
all_symbols   = dataobj.get_all_symbols()
intersectsyms = list(set(all_symbols)&set(portsyms))

#check if the portsyms are all in the symbols provided
bad_symbols = []
if size(intersectsyms) < size(portsyms):
	bad_symbols = list(set(portsyms) - set(intersectsyms))
	print "Warning: portfolio contains symbols that do nont exist: "
	print bad_symbols

# remove the bad_symbols
for i in bad_symbols:
	index = portsyms.index(i)
	portsyms.pop(index)
	portalloc.pop(index)

#configure  the time and read the data

#first, set the time boundaries
endday = dt.datetime(2011,1,1)
startday = endday - dt.timedelta(days=1095)  # 3years back
timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday, endday, timeofday)
close = dataobj.get_data(timestamps, portsyms, "close")

# a quick backtest
rets = close.values.copy()
tsu.fillforward(rets)
tsu.returnize0(rets)            # what is the returnize0 method?

# get the daily returns and total returns
# don't understand how to do the back test
portrets = sum(rets*portalloc, axis=1)          # from the pylab
porttot  = cumprod(portrets+1)                  # method from the pylab, used to cal the cumulated ret
componenttot = cumprod(rets+1,axis=0)

# plot the 
plt.clf()
fig = plt.figure()
fig.add_subplot(111)
plt.plot(timestamps,componenttot)
plt.plot(timestamps,porttot)
names = portsyms
names.append('portfolio')
plt.legend(names)
plt.ylabel('Cumulative Returns')
plt.xlabel('Date')
fig.autofmt_xdate(rotation=45)
savefig('tutorial3.pdf',format='pdf')







	  









 






