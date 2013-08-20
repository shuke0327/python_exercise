import pandas 
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep

"""
Accepts a list of symbols along with start and end date
Returns the Event Matrix which is a pandas Datamatrix
Event matrix has the following structure :
    |IBM |GOOG|XOM |MSFT| GS | JP |
(d1)|nan |nan | 1  |nan |nan | 1  |
(d2)|nan | 1  |nan |nan |nan |nan |
(d3)| 1  |nan | 1  |nan | 1  |nan |
(d4)|nan |  1 |nan | 1  |nan |nan |
...................................
...................................
Also, d1 = start date
nan = no information about any event.
1 = status bit(positively confirms the event occurence)
"""

def findEvents(symbols, startday,endday,close):
	np_eventmat = copy.deepcopy(close)
	for sym in symbols:
		for time in timestamps:
			np_eventmat[sym][time]=np.NAN

	# Generating the Event Matrix
	for symbol in symbols:		
	    for i in range(1,len(close[symbol])):
	    	if close[symbol][i-1] >= 7.0 and close[symbol][i] < 7.0:
             		np_eventmat[symbol][i] = 1  #overwriting by the bit, marking the event
			
	return np_eventmat

def order_generator(eventmatrix,orderfile,symbols):
	buyorder=[]
	sellorder=[]
	# build a index structure for the selldate		
	
	for i in range(len(timestamps)):
		buydate = timestamps[i]
		index = min(len(timestamps)-1,i+5)
		selldate = timestamps[index]  #TODO: make sure the time is ok
		time=timestamps[i]
		for sym in symbols:
			if eventmatrix[sym][time] == 1.0:
				buyorder.append([buydate.year,buydate.month,buydate.day,sym,'Buy',100])
				sellorder.append([selldate.year,selldate.month,selldate.day,sym,'Sell',100])
	
	orders = buyorder
	for elem in sellorder:
		orders.append(elem)
	orders = sorted(orders)
	
	np.savetxt(orderfile,orders,delimiter=',',fmt='%s',newline='\n') #  fmt problem fixed
		

#################################################
################ MAIN CODE ######################
#################################################

symbollist="sp5002012"
orderfile = '/home/shuke0327/python/hw4/orders.csv'

# get timestamps
startday = dt.datetime(2008,1,1)
endday = dt.datetime(2009,12,31)
endday = endday+dt.timedelta(days=1)
timeofday=dt.timedelta(hours=16)
timestamps = du.getNYSEdays(startday,endday,timeofday)

# Get the data from the data store
storename  = "Yahoo" 
closefield = "actual_close"
dataobj    = da.DataAccess('Yahoo')
symbols    = dataobj.get_symbols_from_list(symbollist)
close      = dataobj.get_data(timestamps, symbols, closefield)
close = (close.fillna(method='ffill')).fillna(method='backfill')

# generate orders
eventMatrix = findEvents(symbols,startday,endday,close)
order_generator(eventMatrix,orderfile,symbols)
print 'done'

