#set start and end boundary times.
tsstart = dt.datetime(2004,1,1)
tsend	= dt.datetime(2009,12,31)
timeofday = dt.timedelta(hours=16)
timestamps = du.getNYSEdays(tsstart,tsend,timeofday)

# symbols
symbols = list(np.loadtxt(os.environ['QS']+"/quicksim/strategies/S&P500.csv",dtype='str',delimiter=',', comments='#',skiprows=0))
symbols = symbols[0:20]
symbols.append(_CASH')

#ALLOCATIONS
#Create First Allocation Row values
vals = []
for i in range(21):
	vals.append(randint(0,1000))

# normalize
for i in range(21):
	vals[i]=vals[i]/sum(vals)

alloc = DataFrame(index=[historic.index[0]], data=alloc_vals, columns=symbols)

#Add a row for each new month
last = tsstart
for day in timestamps:
	if (last.month != day,month):
		#create random allocation
		vals = []
		for i in range(21):
			vals.append(random.randint(0,1000))
		for in range(21):
			vals[i] = vals[i]/sum(vals)
	#Append new row
		alloc = alloc.append(DataFrame(index=[day], columns=symbols, dta=[vals]))
	last = day

output = open("allocations.pkl", "wb")
cPickle.dump(alloc,output)

# testing an allocation using the module method
import quickSim as simulator
#setup alloc
#setup historic
funds=simulator.quicksim(alloc,historic,1000)

# testing a strategy using the module
from quicksim import quickSim as qs
strat = os.environ['OS']+"/quicksim/strategies/OneStock.py"
start = dt.datetime(2004,1,1)
end = dt.datetime(2009,1,1)
startval = 1000
fundsmatrix = qs.strat_backtest(strat, start, end, 1,0,startval)













		
		
		
		
		
		
		
		
		
		
		
		
		
			















	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
