#! -*-coding:utf-8 -*-
import urllib2,cookielib,urllib

# login get the cookie
cookie=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
urllib2.install_opener(opener)

#login data
postdata = urllib.urlencode({'username' : 'jingkai27@sina.cn', 'password' : '200630301137','loginsubmit':'登 录'})
login_response= urllib2.urlopen('https://accounts.douban.com/custom_login/',data=postdata)
aa=login_response.read()
print 'aa = \n %s'% aa
pp=urllib2.urlopen('http://book.douban.com/subject_search?search_text=%E5%AE%BD%E5%AE%B9%EF%BC%9A%E6%88%91%E4%B8%8E%E5%9C%B0%E5%9D%9B&cat=1001&swd=1')
bb=pp.read()
fp = open('/home/shuke0327/doubanresult.txt','w')
fp.write(bb)
fp.close()

print 'over'
