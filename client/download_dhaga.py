import urllib2
import os
from threading import Thread

ext='' #extension of file to be downloaded

def fun(start,end,rurl):		#Downloader function
	global ext
	req = urllib2.Request(rurl)
	print start ,end
	req.headers['Range'] = 'bytes=%s-%s' % (start, end)
	site = urllib2.urlopen(req)
	f = open(str(start)+ext, "wb")
	f.write(site.read())
	f.close()
	site.close()
	f = open(str(start)+ext, "rb")
	print "File on disk after download:",len(f.read())
	f.close()

def mgfiles(start):
	global ext
	f=open("final"+ext,"ab")
	f1=open(str(start)+ext,"rb")
	f.write(f1.read())
	f1.close()
	f.close()

def download(rurl,start,end,val_ext):
	global ext
	ext=val_ext
	#site = urllib2.urlopen(rurl)
	#meta= site.info()
	size=end-start+1
	print "Total File size to be downloaded: "+str(size) 
	N=5
	d=(size)/N
	start1=start
	end1=start+d-1
	arr=[[0]*2 for i in range(N)]
	arr[0]=[start1,end1]

	for i in range(1,N):
		if i!=N-1:
			start1=end1+1
			end1=start1+d-1
			arr[i]=[start1,end1]
		else:
			start1=end1+1
			end1=end
			arr[i]=[start1,end1]

	th=[]
	for i in range (N):
		t = Thread(target=fun, args=(arr[i][0],arr[i][1],rurl,))
		th.append(t)

	for i in range(N):
		th[i].start()

	for i in range(N):
		th[i].join()

	for i in range(N):
		mgfiles(arr[i][0])

	for i in range(N):
		os.remove(str(arr[i][0])+ext)
