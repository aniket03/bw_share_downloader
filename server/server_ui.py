import Broad_tcp
import kivy
import time
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
kivy.require('1.8.0') 

a=''
b=''
c=''
txt1=''
txt2=''
txt3=''
def ifyes(instance):
	global a,b,c
	global txt1,txt2,txt3,box
	a=txt1.text
	b=txt2.text
	c=txt3.text
	print a,b,c	
	Broad_tcp.beg_server(a,b,c)
	box.clear_widgets()
	#lbl=Label(Text="File recvd Succesfully")
	#box.add_widget(lbl)
	#return box
	
class MyApp(App):

    def build(self):
		global a,b,c
		global txt1,txt2,txt3,box
		box = BoxLayout(orientation='vertical')
		label1 = Label(text='Enter url of download link\n')
		txt1 = TextInput(text='')
		label2=Label(text='Enter name for file to be saved as\n')
		txt2=TextInput(text='')
		label3=Label(text='Enter extension\n')
		txt3=TextInput(text='')
		print a,b,c
		btn1 = Button(text='Submit', state='normal')
		btn1.bind(on_press=ifyes)
		box.add_widget(label1)
		box.add_widget(txt1)
		box.add_widget(label2)
		box.add_widget(txt2)
		box.add_widget(label3)
		box.add_widget(txt3)
		box.add_widget(btn1)
		return box
		

MyApp().run()
