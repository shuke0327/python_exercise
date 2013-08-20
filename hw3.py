#construct a market simulator

#import the modules
import pandas 
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep

# read the data from the orders.csv file, and extract the time,symbol,share informations
# for cal, we can do it manually.
#result: 
# symbols    =[]
# starttimes =
# endtimes   =
# shares     = 

# read data 

# cal data

# return the data

# Get the data from the data store
storename = "Yahoo" # get data from our daily prices source
# Available field names: open, close, high, low, close, actual_close, volume
closefield = "close" #we use close, namely the adjusted close price
volumefield = "volume"
window = 10

def getData(symbols, startday,endday):

	# Reading the Data for the list of Symbols.	
	timeofday=dt.timedelta(hours=16)
	timestamps = du.getNYSEdays(startday,endday,timeofday)
	dataobj = da.DataAccess("Yahoo")
	# Reading the Data
	close = dataobj.get_data(timestamps, symbols, closefield)
	return close
	

#################################################
################ MAIN CODE ######################
#################################################
#read price data is done
symbols   = ['AAPL','GOOG','XOM','IBM'] #make a list of  the symbols from the orders.csv. 
startday  = dt.datetime(2011,1,1)       #should get from the 
endday    = dt.datetime(2011,3,1)
filepath  = '/home/shuke0327/QSTK/hw3.txt'
stockdata = getData(symbols,startday,endday)









	













