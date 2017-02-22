import kivy
import socket, os
import time
import download_dhaga
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('1.8.0') 

#To get ip of current node
x=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
try:
	x.connect(("gmail.com",80))
	myip=x.getsockname()[0]
except:
	print "Client not connected to internet !!!!!"
	exit
serverip=''
serveraddr=''
totno=''

def ifyes(instance):

	global serveraddr
	clientSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	try:
		clientSocket.sendto('Yes',serveraddr)
	except:
		print "UDP acceptance msg was not sent"
		return
	clientSocket.close()
	
	time.sleep(45)
	print "Client on TCP"
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	clientSocket.bind((myip,50016))
	try:
		clientSocket.connect((serverip,50005))
	except:
		print "Error: Client could not establish TCP connection"
		return
	print "connection established"
	print clientSocket.getsockname()
	ext=clientSocket.recv(1024)
	msg=clientSocket.recv(1024)
	print msg
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

def ifno(instance):
	global serveraddr
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientSocket.sendto('No',serveraddr)
	clientSocket.close()

class MyApp(App):

    def build(self):
	#UDP part
	global serverip
	global serveraddr

	broadSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	broadSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	broadSocket.bind(('<broadcast>',50020))
	msg,serveraddr=broadSocket.recvfrom(2048)
	
	serverip=serveraddr[0]	
	
	print msg
	print "Hello to this world :Testing..... "
	if msg=='':
		print "Error:No msg from server"
		return
	broadSocket.close()
	box = BoxLayout(orientation='vertical')
	label1 = Label(text=msg+'\nEnter Yes/No\n')
	btn1 = Button(text='Yes', state='normal')
	
	btn2 = Button(text='No', state='normal')
	btn1.bind(on_press=ifyes)
	btn2.bind(on_press=ifno)
	box.add_widget(label1)
	box.add_widget(btn1)
	box.add_widget(btn2)
	return box
	
	#time.sleep(10)
def start_client():
	MyApp().run()

start_client()