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
from datetime import datetime, timedelta
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
	        container.grid_columnconfigure(0, weight=1)
	
	        self.frames = {}
	        for F in (HomePage, Register, Capture, Settings, About):
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

		#logo = PhotoImage(file='Logo.png')
	        label = tk.Label(self, text='Welcome to Supa IDS', font=controller.title_font, fg='purple')
#		label.image = logo
	        label.pack(side='top', pady=10)


		spacer = Label(self, text='\n')
		spacer.pack()	


		photoReg = PhotoImage(file='feather.png')
		btnRegister = tk.Button(self, text='  Register', image=photoReg, command=lambda: controller.show_frame('Register'), width=120, font=controller.button_font, compound=LEFT, anchor=W)
		btnRegister.image = photoReg
		btnRegister.pack()

		spacer1 = Label(self, text='\n', height=1)
		spacer1.pack()	

		photoCapture = PhotoImage(file='box.png')
		btnCapture = tk.Button(self, text='  Capture', image=photoCapture, command=lambda: controller.show_frame('Capture'), width=120, font=controller.button_font, compound=LEFT, anchor=W)
		btnCapture.image = photoCapture
		btnCapture.pack()

		spacer2 = Label(self, text='\n', height=1)
		spacer2.pack()		


		photoSettings = PhotoImage(file='settings.png')
		btnSettings = tk.Button(self, text='  Settings', image=photoSettings, command=lambda: controller.show_frame('Settings'), width=120, font=controller.button_font, compound=LEFT, anchor=W)
		btnSettings.image = photoSettings
		btnSettings.pack()

		spacer2 = Label(self, text='\n', height=1)
		spacer2.pack()	

		photoAbout = PhotoImage(file='information.png')
		btnAbout = tk.Button(self, text='  About..', image=photoAbout, command=lambda: controller.show_frame('About'), width=120, font=controller.button_font, compound=LEFT, anchor=W)
		btnAbout.image = photoAbout
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

		lb5 = Label(self, text='\n')
		lb5.pack()	
		
		photoSave = PhotoImage(file='save.png')
		btnSave = tk.Button(self, image=photoSave, text='    Save', command=btnSaveClicked, font=controller.button_font, width=120, compound=LEFT, anchor=W)
		btnSave.image = photoSave
		btnSave.pack()
		
		lb5 = Label(self, text='\n\n')
		lb5.pack()	
		

		photoHome = PhotoImage(file='home.png')
		btnHome = tk.Button(self, image=photoHome, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, compound=LEFT, width=120)
		btnHome.image = photoHome
		btnHome.pack()



class Settings(tk.Frame):
	def __init__(self, parent, controller):
		def is_number(s):
			try:
				float(s)
				return True
			except ValueError:
				return False
		global iface
		global per
		global n
		n = 3
		per = '70'
		
		def showChoice():
			global iface
			iface = str(var.get()).split(' ')[0]

		def btnSaveClicked():
			global iface
			per = entry1.get()
			iface = str(var.get()).split(' ')[0]
			global n
			n = int(variable.get().split(' ')[0])

			if not iface:
				tkmb.showerror('Error','Please choose an interface!')
			elif not per:
				tkmb.showerror('Error','Please enter the percentage!')
			elif not is_number(per):
				tkmb.showerror('Error','Invalid percentage!')
			elif (not float(per) >= 0) or (not float(per) <= 100):
				tkmb.showerror('Error','Invalid percentage!')
			

		tk.Frame.__init__(self, parent)
		self.controller = controller
		lb = Label(self, text='\n')
		lb.pack()

		lbl1 = Label(self, text='Please choose an interface to capture and enter a ratio of anomaly packets ', font=controller.label_font)
		lbl1.pack(padx=5, anchor=W)
		lbl2 = Label(self, text='to receive alert emails', font=controller.label_font)
		lbl2.pack(padx=5, anchor=W)
		

		lb3 = tk.Label(self, text=' Interfaces: ', font='Arial 13 italic bold')
		lb3.pack(anchor=W, pady=5)

		ifaceList = g.all_interfaces()
		global var
		var = StringVar()
		
		for i in ifaceList:
			if i[0] != 'lo':
				rd = tk.Radiobutton(self, text = i[0] + ': ' + i[1], variable = var, value = i, command=showChoice, font=15)
				rd.pack(anchor=W, padx=10)

		if ifaceList[0][0] != 'lo':
			var.set(ifaceList[0])
			iface=ifaceList[0][0]
		else:
			var.set(ifaceList[1])
			iface=ifaceList[1][0]


		lb4 = tk.Label(self, text=' Ratio of anomaly packets: ', font='Arial 13 italic bold')
		lb4.pack(anchor=W, pady=10)
		
		v = StringVar()
		entry1 = Entry(self, textvariable=v, font=18, width=11)
		entry1.pack(padx=15, anchor=W)
		v.set('70')

		lb5 = tk.Label(self, text=' Save log files in: ', font='Arial 13 italic bold')
		lb5.pack(anchor=W, pady=10)

		OPTIONS = ["1 day", "3 days", "7 days", "30 days"]
		variable = StringVar(self)
		variable.set(OPTIONS[1])

		w = OptionMenu(self, variable, *OPTIONS)
		w.pack(anchor=W, padx=15)
		w.config(font=('arial',(12)), width=9)
	
		photoSave = PhotoImage(file='save.png')
		btnSave = tk.Button(self, image=photoSave, text=' Save', command=btnSaveClicked, font=controller.button_font, width=95, compound=LEFT, anchor=W)
		btnSave.pack(pady=20, padx=16, anchor=W)
		btnSave.image = photoSave
		
		photoHome = PhotoImage(file='home.png')
		btnHome = tk.Button(self, image=photoHome, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, compound=LEFT, width=120)
		btnHome.image = photoHome
		btnHome.pack()



class Capture(tk.Frame):

	def __init__(self, parent, controller):

		q = Queue.Queue()

		global isShowTable
		isShowTable = False

		global quit_walking
		quit_walking = Event()

		global quit
		quit = Event()

		def btnStartClicked():	
			btnStart.config(state='disabled')
			btnStop.config(state='normal')
			btnHome.config(state='disabled')	
			btnTrack.config(state='disabled')

			lbtcp.config(text='0')
			lbudp.config(text='0')
			lbicmp.config(text='0')
			lbtotal.config(text='0')
			lbpercent.config(text='Anomaly packets: 0%')
	
			init()
			
			q.queue.clear()

			checkCountFile = os.path.isfile('countpacket.txt')
			if checkCountFile:
				os.remove('countpacket.txt')

			checkResultFile = os.path.isfile('result_data.txt')
			if checkResultFile:
				os.remove('result_data.txt')

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
				if check == False:
					if not q.empty():
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
	
						checkCountFile = os.path.isfile('countpacket.txt')
						checkResultFile = os.path.isfile('result_data.txt')
						if checkCountFile and checkResultFile:
							info = readCountFile()
							sttFile = readResultFile()
							l = file_len('result_data.txt')
							i = 0
							while i >= 0 and i < l:
								stt = sttFile[i].split(',')
								r = info[i].split(',')
								date = datetime.now().strftime('%Y-%m-%d')
								with open('anomaly_log_' + date +'.txt', 'a') as myfile:
									if stt[41] == 'anomaly':
										myfile.write('Duration: ' + r[2] + ' - Protocol: ' + r[3] + ' - Port: ' + r[4] + ' - Service: ' + r[5] + ' - IP Source: ' + r[0] + ' - IP Destination: ' + r[1] + '\n')
								i += 1
	
							#from here user can show tracking table	if there is no available tracking table
							if not isShowTable:
								btnTrack.config(state='normal')
						
				else: 
					try:
						os.remove('sniff.pcap')
					except OSError:
    						print('cannot remove sniff.pcap')
				time.sleep(5)
			quit = Event()
			
		def btnStopClicked():
			btnStart.config(state='normal')
			btnStop.config(state='disabled')
			btnHome.config(state='normal')	

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

			global per
			
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
			
			if curToltal != 0:
				global rate
				rate = curAnomaly*100/curToltal
				print 'anomaly: ' + str(curAnomaly) + ', total: ' + str(curToltal)
				print 'calculated ratio: ' + str(rate)
				
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
			lines = 0
			for line in open(fname):
 				lines += 1
			return lines

		def btnTrackClicked():
			global countPacket
			countPacket = 1
			global win
			btnTrack.config(state='disabled')
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
			btnTrack.config(state='normal')
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
		
		photoTrack = PhotoImage(file='list.png')
		btnTrack = tk.Button(self, image=photoTrack, text='Tracking', command=btnTrackClicked, font=controller.button_font, compound=LEFT, width=120, anchor=W)
		btnTrack.grid(row=7, columnspan=4)
		btnTrack.image = photoTrack
		btnTrack.config(state='disabled')

		photoHome = PhotoImage(file='home.png')
		btnHome = tk.Button(self, image=photoHome, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, compound=LEFT, width=120)
		btnHome.image = photoHome
		btnHome.grid(row=9, columnspan=4)


		v = tk.IntVar()

		photoStart = PhotoImage(file='play.png')
		btnStart = tk.Button(self, image=photoStart, width=120, command=btnStartClicked, font=controller.button_font)
		btnStart.grid(row=1, column=0)
		btnStart.image = photoStart
		btnStart.config(font='Arial 14 bold')

		photoStop = PhotoImage(file='stop.png')
		btnStop = tk.Button(self, image=photoStop, command=btnStopClicked, width=120, font=controller.button_font)
		btnStop.grid(row=1, column=1)
		btnStop.image = photoStop
		btnStop.config(state='disabled', font='Arial 14 bold')

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


class About(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text='About', font=controller.title_font)
	        label.pack(pady=10)

		lbInfo = tk.Label(self, text='IDS Tool is an desktop application built by Incredibility team of FPT University\nContact: supaids.app@gmail.com\n', font=controller.label_font)
		lbInfo.config(justify=LEFT)
		lbInfo.pack()

	        photoHome = PhotoImage(file='home.png')
		btnHome = tk.Button(self, image=photoHome, text='Home page', command=lambda: controller.show_frame('HomePage'), font=controller.button_font, compound=LEFT, width=120)
		btnHome.image = photoHome
		btnHome.pack()
		
	
if __name__ == '__main__':
	app = SampleApp()
	app.geometry('800x500')
	app.title('Supa IDS')

	global quit_walking
	quit_walking = Event()

	global quit
	quit = Event()

	global stopCheckLog
	stopCheckLog = Event()

	def checkLogFile(): #thread check log file
		global stopCheckLog
		while not stopCheckLog.is_set():
			global n
			print n	
			date_n_days_ago = datetime.now() - timedelta(days=n)
		
			check = os.path.isfile('anomaly_log_'+date_n_days_ago.strftime('%Y-%m-%d')+'.txt')
			if check:
				try:
					os.remove('anomaly_log_'+date_n_days_ago.strftime('%Y-%m-%d')+'.txt')
				except OSError:
    					print('Cannot remove log file')
			totalSleepCount = 86400
			while totalSleepCount > 0:
				time.sleep(5)
				totalSleepCount -= 5
				if stopCheckLog.is_set():
					totalSleepCount = 0

		stopCheckLog = Event()
		
	def on_closing():
		global quit_walking
		quit_walking.set()

		global quit
		quit.set()

		global stopCheckLog
		stopCheckLog.set()



		jvm.stop()
		run.stopSnort()
		app.destroy()
	

	muy = Thread(target=checkLogFile)
	muy.start()

	app.protocol('WM_DELETE_WINDOW', on_closing)

	app.mainloop()
