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
						file.write(username+','+mail+',') 
						file.close()
						tkmb.showinfo('Success','Success')	
				
			
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
		
		lb5 = Label(self, text='\n\n')
		lb5.pack()	
		
		button = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		button.pack()


class ChooseIface(tk.Frame):
	def __init__(self, parent, controller):
		def is_number(s):
			try:
				float(s)
				return True
			except ValueError:
				return False

		def showChoice():
			global iface
			iface = str(var.get()).split(' ')[0]

		def btnSaveClicked():
			global iface
			iface = str(var.get()).split(' ')[0]
			global per
			per = entry1.get()
			if not iface:
				tkmb.showerror('Error','Please choose an interface!')
			elif not per:
				tkmb.showerror('Error','Please enter the percentage!')
			elif not is_number(per):
				tkmb.showerror('Error','Invalid percentage!')
			elif (not float(per) >= 0) or (not float(per) <= 100):
				tkmb.showerror('Error','Invalid percentage!')
			else:
				btnNext.config(state='normal')

		tk.Frame.__init__(self, parent)
		self.controller = controller
		lb = Label(self, text='\n')
		lb.pack()

		lbl1 = Label(self, text='Please choose an interface to capture and enter a ratio of anomaly packets ', font=controller.label_font)
		lbl1.pack(padx=5, anchor=W)
		lbl2 = Label(self, text='to receive alert emails', font=controller.label_font)
		lbl2.pack(padx=5, anchor=W)
		

		lb3 = tk.Label(self, text=' Interfaces: ', font='Arial 13 italic bold')
		lb3.pack(anchor=W, pady=10)

		ifaceList = g.all_interfaces()
		var = StringVar()
		for i in ifaceList:
			if i[0] != 'lo':
				rd = tk.Radiobutton(self, text = i[0] + ': ' + i[1], variable = var, value = i, command=showChoice, font=15)
				rd.pack(anchor=W)

		lb4 = tk.Label(self, text=' Ratio of anomaly packets: ', font='Arial 13 italic bold')
		lb4.pack(anchor=W, pady=10)

		entry1 = Entry(self, font=18, width=11)
		entry1.pack(padx=15, anchor=W)
	
		btnSave = tk.Button(self, text='Save', command=btnSaveClicked, font=controller.button_font, width=10)
		btnSave.pack(pady=20, padx=10, anchor=W)

		btnNext = tk.Button(self, text='Next', command=lambda: controller.show_frame('Capture'), font=controller.button_font, width=10)
		btnNext.pack(pady=20, padx=10)
		btnNext.config(state='disabled')
		
		button = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		button.pack()


class Capture(tk.Frame):

	def __init__(self, parent, controller):

		q = Queue.Queue()

		global isShowTable
		isShowTable = False

		global quit_walking
		quit_walking = Event()

		global quit
		quit = Event()

		def btnStartWithoutSnortClicked():	
			btnStartWithoutSnort.config(state='disabled')
			btnStartWithSnort.config(state='disabled')
			btnStop.config(state='normal')
			btnShow.config(state='disabled')

			lbtcp.config(text='0')
			lbudp.config(text='0')
			lbicmp.config(text='0')
			lbtotal.config(text='0')
			lbpercent.config(text='Anomaly packets: 0%')
	
			init()
			
			q.queue.clear()

			#start a thread to capture and put packets into queue
			alan = Thread(target=walkerLoop)
			alan.start()

			#start a thread to get packets out of queue and analyse
			alang = Thread(target=checkPcap)
			alang.start()

		def walkerLoop(): #thread capture
			global quit_walking
			while not quit_walking.is_set():
				cap = sniff(count=6000,timeout=10,iface=iface)
				while not cap:
					cap = sniff(count=6000,timeout=10,iface=iface)
				q.put(cap)
			quit_walking = Event()

		def checkPcap(): #thread analyse
			global isShowTable

			global quit
			while not quit.is_set():
				check = os.path.isfile('sniff.pcap')
				if check == False :
					a = q.get() #if empty, wait until a flow is put in queue
					wrpcap('sniff.pcap', a)
					
					e.bro()
					e.sort()
					e.exportFile() #export countpacket.txt and trafAld.arff

					w = wk('KDDTrain+.arff', 'trafAld.arff')
					w.start() #export result_data.txt

					#show table after analysing
					if isShowTable:
						reloadTable()

					#show number of packets on app
					try:
						count()
					except IOError:
						pass

					#save anomaly packet to anomaly_log.txt
					info = readCountFile()
					sttFile = readResultFile()
					l = file_len('result_data.txt')
					i = 0
					while i >= 0 and i < l:
						stt = sttFile[i].split(',')
						r = info[i].split(',')
						with open('anomaly_log.txt', 'a') as myfile:
							if stt[41] == 'anomaly':
								myfile.write('Duration: ' + r[2] + ' - Protocol: ' + r[3] + ' - Port: ' + r[4] + ' - Service: ' + r[5] + ' - IP Source: ' + r[0] + ' - IP Destination: ' + r[1] + '\n')
						i += 1

					#from here user can show tracking table	if there is no available tracking table
					if not isShowTable:
						btnShow.config(state='normal')
					
				else: 
					try:
						os.remove('sniff.pcap')
					except OSError:
    						print('cannot remove sniff.pcap')
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
			
			#stop capture
			global quit_walking
			quit_walking.set()

			#stop analyse
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
			global anomalycount
			anomalycount = 0

		def count():			
			l = file_len('countpacket.txt')
			file = open('countpacket.txt','r').read().splitlines()
			
			global total
			curToltal = int(file[l-4])
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


			sttFile = readResultFile()
			l2 = file_len('result_data.txt')
			global anomalycount
			curAnomaly = 0
			i = 0			
			while i < l2:
				stt = sttFile[i].split(',')
				if stt[41] == 'anomaly':
					anomalycount += 1
					curAnomaly += 1
				i += 1
			percentage = anomalycount*100/total
			lbpercent.config(text='Anomaly packets: ' + str(percentage) +'%')

			global rate
			rate = curAnomaly*100/curToltal
			print 'anomaly: ' + str(curAnomaly) + ', total: ' + str(curToltal)
			print 'calculated ratio: ' + str(rate)
			global per
			print float(per)
			if float(per) <= rate:
				file = open('user_info.txt', 'r') 
				info = file.read().split(',')
				name = info[0]
				subject = 'Supa IDS Alert!'
				msg = 'Hi ' + name + ',\nThe ratio of anomaly packets is higher than the ratio that you allowed. Please check your system now.\n\nRegards,\nSupa IDS Team'
				mail = info[1]
 				send_email.send_email(subject, mail, msg)

		def readCountFile():
			file = open('countpacket.txt','r')	
			info = file.read().split('\n')
			return info
		

		def readResultFile():
			file = open('result_data.txt','r')
			sttFile = file.read().split('\n')
			return sttFile
			
		def file_len(fname):
			with open(fname) as f:
				for i, l in enumerate(f):
					pass
			return i + 1

		def btnTrackClicked():
			global countPacket
			countPacket = 1
			global win
			btnShow.config(state='disabled')
			global isShowTable
			isShowTable = True
			global table
			win = tk.Toplevel()
			win.title('Tracking Screen')
			table = display.Table(win, ['No.', 'Duration', 'Protocol', 'Port', 'Service', 'IP Source', 'IP Destination', 'Status'])
			table.grid(sticky=W+E+N+S)
			win.geometry('%sx%s'%(560,530))
			win.protocol('WM_DELETE_WINDOW', btnExit)

			reloadTable()


		def reloadTable():
			global countPacket
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
					table.insert_row([countPacket,r[2],r[3],r[4],r[5],r[0],r[1],stt[41]])
					i += 1
					countPacket += 1
				except IndexError:
					i = -1
			win.update()

		def btnExit():
			global isShowTable
			isShowTable = False
			btnShow.config(state='normal')
			win.destroy()
			
			

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
		self.rowconfigure(9, pad=10, weight=1)


		label = tk.Label(self, text='Capture', font=controller.title_font)
		label.grid(row=0, columnspan=4, sticky=NSEW)
		
		btnShow = tk.Button(self, text='Tracking', command=btnTrackClicked, font=controller.button_font, width=10)
		btnShow.grid(row=7, columnspan=4)
		btnShow.config(state='disabled')

		btnBack = tk.Button(self, text='Back', command=lambda: controller.show_frame('ChooseIface'), font=controller.button_font, width=10)
		btnBack.grid(row=8, columnspan=4)

		btnHome = tk.Button(self, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, width=10)
		btnHome.grid(row=9, columnspan=4)


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
		lbpercent = tk.Label(self, text='Anomaly packets: 0%', font=15, fg='red')	
		lbpercent.grid(row=5, column=3)
		
		label = tk.Label(self, text='\n\n\n\n', font=controller.title_font)
		label.grid(row=6, columnspan=4, sticky=NSEW)

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
	global quit_walking
	quit_walking = Event()

	global quit
	quit = Event()
		
	def on_closing():
		global quit_walking
		quit_walking.set()

		global quit
		quit.set()

		jvm.stop()
		run.stopSnort()
		app.destroy()
	

	app.protocol('WM_DELETE_WINDOW', on_closing)

	app.mainloop()
