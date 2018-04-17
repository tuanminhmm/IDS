from Tkinter import *
import Tkinter as tk            
import tkFont  as tkfont
import tkMessageBox as tkmb

import time
import socket
import re
import os
import subprocess
import Queue

from threading import Event
from threading import Thread
from scapy.all import *


import send_email
import getIface as g
import exportFiles as e
import runsnort as run
import displayTable as display
from train_test import wekaTrainTest as wk
import weka.core.jvm as jvm

class SampleApp(tk.Tk):
	def __init__(self, *args, **kwargs):
	        tk.Tk.__init__(self, *args, **kwargs)
	
	        self.title_font = tkfont.Font(family='Arial', size=24, weight='bold')
	        self.button_font = tkfont.Font(size=12)
	        self.label_font = tkfont.Font(size=12)

	        container = tk.Frame(self)
	        container.pack(fill='both', expand=True)
	        #container.grid_rowconfigure(0, weight=1)
	        container.grid_columnconfigure(0, weight=1)
	
	        self.frames = {}
	        for F in (HomePage, Register, ChooseIface, Capture, Graph, About):
	            page_name = F.__name__
	            frame = F(parent=container, controller=self)
	            self.frames[page_name] = frame
	
	            frame.grid(row=0, column=0, sticky='nsew')
	
	        self.show_frame('HomePage')

	def show_frame(self, page_name):
	        frame = self.frames[page_name]
	        frame.tkraise()


	
class HomePage(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text='Welcome to Supa IDS', font=controller.title_font, fg='purple')
	        label.pack(side='top', pady=10)


		spacer = Label(self, text='\n')
		spacer.pack()	

		btnRegister = tk.Button(self, text='Register', command=lambda: controller.show_frame('Register'), width=10, font=controller.button_font)
		btnRegister.pack()

		spacer1 = Label(self, text='\n', height=1)
		spacer1.pack()	

		btnChooseIface = tk.Button(self, text='Capture', command=lambda: controller.show_frame('ChooseIface'), width=10, font=controller.button_font)
		btnChooseIface.pack()

		spacer2 = Label(self, text='\n', height=1)
		spacer2.pack()	

		btnGraph = tk.Button(self, text='Show Graph', command=lambda: controller.show_frame('Graph'), width=10, font=controller.button_font)
		btnGraph.pack()	

		spacer3 = Label(self, text='\n', height=1)
		spacer3.pack()	

		btnAbout = tk.Button(self, text='About..', command=lambda: controller.show_frame('About'), width=10, font=controller.button_font)
		btnAbout.pack()

		
class Register(tk.Frame):
	def __init__(self, parent, controller):

		def btnSaveClicked():
			if not entry1.get():
				tkmb.showerror('Error','Please enter your name!')				
			else:
				if not entry2.get():
					tkmb.showerror('Error','Please enter your email!')					
				else:
					if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', entry2.get()):
						tkmb.showerror('Error','Your email is not valid!')
					else:
						username = entry1.get()
						mail = entry2.get()

						file = open('user_info.txt','w') 
						file.write(username+','+mail) 
						file.close()
						tkmb.showinfo('Success','Success')	
				

		#def btnSendClicked():
			
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text='Register', font=controller.title_font)
		label.pack(side='top', fill='x', pady=10)

		frame1 = Frame(self)
		frame1.pack(fill=X)
		lbl1 = Label(frame1, text='Name', width=6, font=controller.label_font)
		lbl1.pack(side=LEFT, padx=5, pady=5)

		entry1 = Entry(frame1, font=18)
		entry1.focus()
		entry1.pack(fill=X, padx=15, expand=True)


		frame2 = Frame(self)
		frame2.pack(fill=X)
		lbl2 = Label(frame2, text='Email', width=6, font=controller.label_font)
		lbl2.pack(side=LEFT, padx=5, pady=5)
		
		entry2 = Entry(frame2, font=18)
		entry2.pack(fill=X, padx=15, expand=True)


		file = open('user_info.txt', 'r') 
		info = file.read().split(',')

 		if info[0]:
			entry1.insert(0, info[0])
			entry2.insert(0, info[1])

		btnSave = tk.Button(self, text='Save', command=btnSaveClicked, font=controller.button_font)
		btnSave.pack()
		
		#btnSend = tk.Button(self, text='Send', command=btnSendClicked, font=controller.button_font)
		#btnSend.pack()
		
		lb5 = Label(self, text='\n\n')
		lb5.pack()	
		
		button = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		button.pack()


class ChooseIface(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller

		label = tk.Label(self, text='Choose an interface: ', font=25)
		label.pack(anchor=W, pady=10)
		
		global iface
		ifaceList = g.all_interfaces()

		def showChoice():
			global iface
			iface = str(var.get()).split(' ')[0]
			btnCapture.config(state='normal')

		var = StringVar()
		for i in ifaceList:
			if i[0] != 'lo':
				rd = tk.Radiobutton(self, text = i[0] + ': ' + i[1], variable = var, value = i, command=showChoice, font=15)
				rd.pack(anchor=W)
		
		btnCapture = tk.Button(self, text='Capture', command=lambda: controller.show_frame('Capture'), font=controller.button_font)
		btnCapture.pack(anchor=W, pady=20, padx=10)
		btnCapture.config(state='disabled')
		
		button = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		button.pack()


class Capture(tk.Frame):

	def __init__(self, parent, controller):

		global quit_walking
		quit_walking = Event()

		global quit
		quit = Event()

		q = Queue.Queue()

		def btnStartWithoutSnortClicked():
			btnStartWithoutSnort.config(state='disabled')
			btnStartWithSnort.config(state='disabled')
			btnStop.config(state='normal')

			init()

			alan = Thread(target=walkerLoop)
			alan.start()

			alang = Thread(target=checkPcap)
			alang.start()

		def walkerLoop():
			global quit_walking
			while not quit_walking.is_set():
				cap = sniff(count=100,timeout=20,iface=iface)
				q.put(cap)
			quit_walking = Event()

		def checkPcap():
			pcapfile = 'sniff.pcap'
			global quit
			while not quit.is_set():
				check = os.path.isfile(pcapfile)
				if check == False:
					a = q.get()
					wrpcap(pcapfile, a)
					
					e.bro()
					e.sort()
					e.exportFile()

					w = wk('KDDTrain+.arff', 'trafAld.arff')
					w.start()
					info = readCountFile()
					sttFile = readResultFile()
					btnShow.config(state='normal')
					l = file_len('countpacket.txt') 
					i = 0
					while i >= 0 and i <= l-4:
						try:
							stt = sttFile[i].split(',')
							r = info[i].split(',')
							if stt[41] == 'anomaly':
								with open('anomal_log.txt', 'a') as myfile:
									myfile.write('Duration: ' + r[2] + ' - Protocol: ' + r[3] + ' - Port: ' + r[4] + ' - Service: ' + r[5] + ' - IP Source: ' + r[0] + ' - IP Destination: ' + r[5] + '\n')
							i += 1
						except IndexError:
							i = -1
	
					try:
						count()
					except IOError:
						pass
				else: 
					try:
						os.remove(pcapfile)
					except OSError:
    						pass
				time.sleep(5)
			quit = Event()


		def btnStartWithSnortClicked():
			btnStartWithoutSnort.config(state='disabled')
			btnStartWithSnort.config(state='disabled')
			btnStop.config(state='normal')

			run.runSnort()
			btnStartWithoutSnortClicked()

			
		def btnStopClicked():
			btnStartWithoutSnort.config(state='normal')
			btnStartWithSnort.config(state='normal')
			btnStop.config(state='disabled')
	
			run.stopSnort()
			
			global quit_walking
			quit_walking.set()

			global quit
			quit.set()
			
		def init():			
			global total
			total = 0
			global tcp 
			tcp = 0
			global udp
			udp = 0
			global icmp 
			icmp = 0

		def count():
			l = file_len('countpacket.txt')
			file = open('countpacket.txt','r').read().splitlines()

			global total
			total += int(file[l-4])
			lbtotal.config(text=total)
					
			global tcp
			tcp += int(file[l-3])
			lbtcp.config(text=tcp)
			
			global udp
			udp += int(file[l-2])
			lbudp.config(text=udp)
			
			global icmp
			icmp += int(file[l-1])
			lbicmp.config(text=icmp)

		def readCountFile():
			file = open('countpacket.txt','r')	
			info = file.read().split('\n')
			return info
		

		def readResultFile():
			try:
				file = open('result_data.txt','r')
			except IOError:
				pass
			sttFile = file.read().split('\n')
			return sttFile
			
		def file_len(fname):
			with open(fname) as f:
				for i, l in enumerate(f):
					pass
			return i + 1

		def dis():
			win = tk.Toplevel()
			win.title('Tracking Screen')
			btnShow.config(state='disabled')
			
			table = display.Table(win, ['Duration', 'Protocol', 'Port', 'Service', 'IP Source', 'IP Destination', 'Status'])
			table.grid(sticky=W+E+N+S)
			info = readCountFile()
			sttFile = readResultFile()
			try:
				l = file_len('countpacket.txt') 
			except IOError:
				pass
			i = 0
			while i >= 0 and i <= l-4:
				try:
					stt = sttFile[i].split(',')
					r = info[i].split(',')
					table.insert_row([r[2],r[3],r[4],r[5],r[0],r[1],stt[41]])
					i += 1
				except IndexError:
					i = -1
			win.update()
			win.geometry('%sx%s'%(win.winfo_reqwidth(),530))
			
			def close_clicked(win):
    				print 'nice'
				win.destroy()
			
			win.wm_protocol('WM_DELETE_WINDOW', lambda win=win: close_clicked(win))
		



		tk.Frame.__init__(self, parent)
		self.controller = controller

		self.columnconfigure(0, pad=10, weight=1)
    		self.columnconfigure(1, pad=10, weight=1)
		self.columnconfigure(2, pad=10, weight=1)
		self.columnconfigure(3, pad=10, weight=1)
        
		self.rowconfigure(0, pad=10, weight=1)
		self.rowconfigure(1, pad=10, weight=1)
		self.rowconfigure(2, pad=10, weight=1)
		self.rowconfigure(3, pad=10, weight=1)
		self.rowconfigure(4, pad=10, weight=1)
		self.rowconfigure(5, pad=10, weight=1)
		self.rowconfigure(6, pad=10, weight=1)
		self.rowconfigure(7, pad=10, weight=1)
		self.rowconfigure(8, pad=10, weight=1)


		label = tk.Label(self, text='Capture', font=controller.title_font)
		label.grid(row=0, columnspan=4, sticky=NSEW)
		
		btnShow = tk.Button(self, text='Tracking', command=dis, font=controller.button_font, width=10)
		btnShow.grid(row=6, columnspan=4)
		btnShow.config(state='disabled')

		btnBack = tk.Button(self, text='Back', command=lambda: controller.show_frame('ChooseIface'), font=controller.button_font, width=10)
		btnBack.grid(row=7, columnspan=4)

		btnHome = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		btnHome.grid(row=8, columnspan=4)


		v = tk.IntVar()


		btnStartWithSnort = tk.Button(self, text='Start (recommended)', command=btnStartWithSnortClicked, width=17, font=controller.button_font, fg='green')
		btnStartWithSnort.grid(row=1, column=0)
		btnStartWithSnort.config(font='Arial 14 bold')
		
		btnStartWithoutSnort = tk.Button(self, text='Start Without Snort', width=17, command=btnStartWithoutSnortClicked, font=controller.button_font, fg='green')
		btnStartWithoutSnort.grid(row=1, column=1)
		btnStartWithoutSnort.config(font='Arial 14 bold')

		btnStop = tk.Button(self, text='Stop', command=btnStopClicked, width=17, font=controller.button_font, fg='red')
		btnStop.grid(row=1, column=3)
		btnStop.config(state='disabled', font='Arial 14 bold')

#		btnCheckFile = tk.Button(self, text='count', command=init, width=15, font=controller.button_font)
#		btnCheckFile.grid(row=6, columnspan=4)		

#		label = tk.Label(self, text='\n', font=controller.title_font)
#		label.grid(row=2, columnspan=4, sticky=NSEW)

		tcptitle = tk.Label(self, text='TCP PACKETS', font=15)
		tcptitle.grid(row=3, column=0)
		udptitle = tk.Label(self, text='UDP PACKETS', font=15)
		udptitle.grid(row=3, column=1)
		icmptitle = tk.Label(self, text='ICMP PACKETS', font=15)
		icmptitle.grid(row=3, column=2)
		totaltitle = tk.Label(self, text='TOTAL', font=15, fg='blue')
		totaltitle.grid(row=3, column=3)

		lbtcp = tk.Label(self, text='0', font=15)
		lbtcp.grid(row=4, column=0)
		lbudp = tk.Label(self, text='0', font=15)
		lbudp.grid(row=4, column=1)
		lbicmp = tk.Label(self, text='0', font=15)
		lbicmp.grid(row=4, column=2)
		lbtotal = tk.Label(self, text='0', font=15, fg='blue')
		lbtotal.grid(row=4, column=3) 		
		
		label = tk.Label(self, text='\n\n\n\n\n', font=controller.title_font)
		label.grid(row=5, columnspan=4, sticky=NSEW)

class Graph(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text='Graph', font=controller.title_font)
	        label.pack(side='top', fill='x', pady=10)
	        button = tk.Button(self, text='Home page',
	                           command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
	        button.pack()

class About(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text='About', font=controller.title_font)
	        label.pack(pady=10)

		lbInfo = tk.Label(self, text='IDS Tool is an desktop application built by: ...\nVisit our website at: www.idstool.com\n', font=controller.label_font)
		lbInfo.config(justify=LEFT)
		lbInfo.pack()

	        button = tk.Button(self, text='Home page',
	                           command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
	        button.pack()
		
	
if __name__ == '__main__':
	app = SampleApp()
	app.geometry('800x530')
	app.title('Supa IDS')
		
	def on_closing():
		jvm.stop()
		run.stopSnort()
		app.destroy()
	

	app.protocol('WM_DELETE_WINDOW', on_closing)

	app.mainloop()
