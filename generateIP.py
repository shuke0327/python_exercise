def generateRandom(rangeFrom, rangeTo):
	import random
	return random.randint(rangeFrom, rangeTo)

def generageMassiveIPAddr(fileLocation,LineNum):
	IP = []
	file_handler = open(fileLocation,'a+')
	for i in range(LineNum):
		IP.append('10.197.' + str(generateRandom(0,255)) + '.'\
				+ str(generateRandom(0,255)) + '\n')
	file_handler.writelines(IP)
	file_handler.close()

if __name__ == '__main__':
	from time import ctime
	print ctime()
	for i in range(10):
		print ' ' + str(i) + ": " + ctime()
		generageMassiveIPAddr('/home/shuke0327/python/test/IP.txt', 1000000)
	print ctime()

