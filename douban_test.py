# just for test of a tool used for converge the campus reading history
# -*- coding:utf-8 -*-
import numpy as nu
import extract
import requests
import urllib2,cookielib,urllib

#sort the record
def getrecord(filepath):
	bookrecords = nu.loadtxt(filepath,dtype='S50,S20', delimiter=':',comments='#',)
	bookrecords = sorted(bookrecords,key=lambda x: x[1])
	bookname   = []
	borrowdate = []
	for record in bookrecords:
		bookname.append(record[0])
		borrowdate.append(record[1])
	totalrecord = len(bookname)	
	for i in range(0,totalrecord):
		bookname[i]   = str(bookname[i])
		borrowdate[i] = str(borrowdate[i])
	return (bookname,borrowdate,totalrecord)

# next step: use the spider to get the id of book 
def doubansearch(bookname):
	#website = 'http://book.douban.com/subject_search?search_text=%s&cat=1003'%bookname
	website = 'https://api.douban.com/v2/book/search?q=%s&cat=1003&start=0&count=1' %bookname
	search_result = requests.get(website)
	# need to find the id
	idrecord = []
	if search_result.status_code == 200:
		content = search_result.text
		index = content.find('id')
		start_pos = int(int(index)+5)
		end_pos   = start_pos+7
		bookid = content[start_pos:end_pos]
		idrecord.append(bookid)
	else:
		return False
	return idrecord

	


# main function
if __name__ == '__main__':
	filepath  = '/home/shuke0327/python/readhistory.csv'
	books, borrowdate,totalrecord = getrecord(filepath)
	search = []
	
	for i in range(0,2):
		website = 'https://api.douban.com/v2/book/search?q=%s&cat=1003&start=0&count=1' %books[i]
	search_result = requests.get(website)
	print search_result.status_code



'''
	for i in range(0,3):
		print "%d of %d is being processed " %(i,totalrecord)
		bookid = doubansearch(books[i])
		search.append(bookid)
		print bookid
	
	print search
	print "hello"
'''


	





 
	
