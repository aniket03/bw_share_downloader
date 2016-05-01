import os,nmap
import socket,thread,threading
import urllib2
import time
import download_dhaga

rurl=''		#download link
fname=''	#file to be saved as
ext=''		#extension of file
myip=''		#ip extension of my node
live_ips=[]
size=''

yescount=0
th=[]

def handleclient(connsocket,start,end,i):
	global rurl,ext
	print connsocket.getsockname()
	print connsocket.recv(1024)
	msg=rurl+' '+str(start)+' '+str(end)+' '+str(i)
	print msg,ext
	try:
		connsocket.send(ext)
		connsocket.send(msg)
	except:
		print "URL and ext message not sent"
	print "Message sent successfully"
	f=open(str(i)+ext,'wb')
	while True:
		l=connsocket.recv(1024)
		if not l:
			break
		f.write(l)
	f.close()
	print "Recvd succesfully"
	connsocket.close()

def mgfiles(ind):
	f=open(fname+ext,"ab")
	f1=open(str(ind)+ext,"rb")
	f.write(f1.read())
	f1.close()
	f.close()

def acc_tcp():
	#Divide file into ranges
	global yescount	
	N=yescount
	d=(size)/N
	start1=0
	end1=d-1
	arr=[[0]*2 for i in range(N)]
	arr[0]=[start1,end1]

	for i in range(1,N):
		if i!=N-1:
			start1=end1+1
			end1=start1+d-1
			arr[i]=[start1,end1]
		else:
			start1=end1+1
			end1=size-1
			arr[i]=[start1,end1]
	#Set server host,port and socket
	global myip 
	host = myip
	port = 50005                    
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)      
	# Bind the socket to the port
	s.bind((host, port))            
	s.listen(5)
	print 'Server binded and ready to use for TCP'
	i=0
	while i<yescount:
		try:
			s.settimeout(80)
			connsocket,addr = s.accept()
			print addr
			t = threading.Thread(target=handleclient, args=(connsocket,arr[i][0],arr[i][1],i,))
			th.append(t)
			i=i+1
		except socket.timeout:
			#In case the client under consideration fails to make TCP connection
			print "Problem1: Server itself downloads chunk "+str(arr[i][0])+"-" +str(arr[i][1])
			download_dhaga.download(rurl,arr[i][0],arr[i][1],ext)
			os.rename('final'+ext,str(i)+ext) 
			mgfiles(i)
			os.remove(str(i)+ext)
			i=i+1
	
	for i in range(len(th)):
		th[i].start()
		#th[i].join()
	
	for i in range(len(th)):
		th[i].join(60.0)
		
		if th[i].isAlive():
			print "Problem2: Server itself downloads chunk "+str(arr[i][0])+"-" +str(arr[i][1])
			download_dhaga.download(rurl,arr[i][0],arr[i][1],ext)
			os.rename('final'+ext,str(i)+ext) 
	
	for i in range(len(th)):
		mgfiles(i)
	
	for i in range(len(th)):
		os.remove(str(i)+ext)
	s.close()

def broad_udp():

	host = myip
	port = 50005
	message="Can you help in download"

	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	s.bind((host,port))
	s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	s.sendto(message,('<broadcast>',50008))
	s.sendto(message,('<broadcast>',50020))
	s.close()

	ini=time.time()
	global yescount
	
	while time.time()-ini<= 40:
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
			s.bind((host,port))
			s.settimeout(6)
			reply,caddr=s.recvfrom(2048)
			print caddr
			if reply=='Yes' or reply=='yes':
				yescount=yescount+1
			s.close()
		except socket.timeout:
			print "caught timeout"
	print yescount

def  beg_server(rurl_val,fname_val,ext_val):	#rurl url of file to be downloaded
	global rurl,fname,ext,myip,live_ips,size
	rurl=rurl_val
	fname=fname_val
	ext=ext_val

	#To get ip of current node
	x=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		x.connect(("gmail.com",80))
		myip=x.getsockname()[0]
	except:
		print "Server not connected to internet !!!!!"
		return
	#size of file 
	site = urllib2.urlopen(rurl)
	meta= site.info()
	size= meta.getheaders("Content-Length")[0]
	size=int(size)
	print "Total File size to be downloaded: "+str(size)

	#myip='10.42.0.1'
	#Find live nodes
	'''
	temp = []
	temp = myip.split('.')
	stip=temp[0]+'.'+temp[1]+'.'+temp[2]+'.'+'0/24'    #start ip/24
	
	nm = nmap.PortScanner()
	nm.scan(hosts=stip, arguments='-n -sP -PE -PA21,23,80,3389')
	hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
	for host, status in hosts_list:
		live_ips.append(str(host))
		print(str(host)+":"+str(status))
	'''
	broad_udp()
	acc_tcp()
