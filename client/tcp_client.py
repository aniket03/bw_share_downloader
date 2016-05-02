import socket, os
import time
import download_dhaga

#To get ip of current node
x=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
	x.connect(("gmail.com",80))
	myip=x.getsockname()[0]
except:
	print "Client not connected to internet !!!!!"
	return 
#UDP part
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind((myip,50008))
msg,serveraddr=clientSocket.recvfrom(2048)
serverip=serveraddr[0]
msg,totno=msg.split('#')		#totno represents total no of nodes on network
print msg
totno=int(totno)
res=raw_input("Enter Yes/No\n")
clientSocket.sendto(res,serveraddr)
clientSocket.close()

if(res == "Yes"):
	#To set client address and port
	#serveraddr=(myip,50005)		#myip to be replace with server addr
	time.sleep(9*totno)
	print "Client on TCP"
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	clientSocket.connect((serverip,50005))
	ext=clientSocket.recv(1024)
	msg=clientSocket.recv(1024)
	#print msg
	rurl,st,en,i=msg.split()
	start=int(st)
	end=int(en)
	ind=int(i)

	download_dhaga.download(rurl,start,end,ext)
	
	f=open('final'+ext,'rb')
	l=f.read(1024)
	while l:
		clientSocket.send(l)
		l=f.read(1024)
	os.remove('final'+ext)
	clientSocket.close()
