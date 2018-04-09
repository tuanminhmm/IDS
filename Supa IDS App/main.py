import Tkinter as tk            
import tkFont  as tkfont
import tkMessageBox as tkmb
import datetime
now = datetime.datetime.now()
import re
from Tkinter import *
import send_email
import socket
import runsnort as run
from threading import Event
from threading import Thread
import os
import Queue
from scapy.all import *
#import sql

class SampleApp(tk.Tk):
	def __init__(self, *args, **kwargs):
	        tk.Tk.__init__(self, *args, **kwargs)
	
	        self.title_font = tkfont.Font(family='Arial', size=24, weight="bold")
	        self.button_font = tkfont.Font(size=12)
	        self.label_font = tkfont.Font(size=12)

	        container = tk.Frame(self)
	        container.pack(fill="both", expand=True)
	        #container.grid_rowconfigure(0, weight=1)
	        container.grid_columnconfigure(0, weight=1)
	
	        self.frames = {}
	        for F in (HomePage, Capture, Graph, About, Register):
	            page_name = F.__name__
	            frame = F(parent=container, controller=self)
	            self.frames[page_name] = frame
	
	            frame.grid(row=0, column=0, sticky="nsew")
	
	        self.show_frame("HomePage")

	def show_frame(self, page_name):
	        frame = self.frames[page_name]
	        frame.tkraise()


	
class HomePage(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text="Welcome to Supa IDS", font=controller.title_font, fg="purple")
	        label.pack(side="top", pady=10)


		spacer = Label(self, text="\n")
		spacer.pack()	

		btnRegister = tk.Button(self, text="Register", command=lambda: controller.show_frame("Register"), width=10, font=controller.button_font)
		btnRegister.pack()

		spacer1 = Label(self, text="\n", height=1)
		spacer1.pack()	

		btnCapture = tk.Button(self, text="Capture", command=lambda: controller.show_frame("Capture"), width=10, font=controller.button_font)
		btnCapture.pack()

		spacer2 = Label(self, text="\n", height=1)
		spacer2.pack()	

		btnGraph = tk.Button(self, text="Show Graph", command=lambda: controller.show_frame("Graph"), width=10, font=controller.button_font)
		btnGraph.pack()	

		spacer3 = Label(self, text="\n", height=1)
		spacer3.pack()	

		btnAbout = tk.Button(self, text="About..", command=lambda: controller.show_frame("About"), width=10, font=controller.button_font)
		btnAbout.pack()

		
class Register(tk.Frame):
	def __init__(self, parent, controller):

		def btnSaveClicked():
			file = open('user_info.txt', 'r') 
			info = file.read() 
			try:
				uname = info.split(',')[1]
				if not entry2.get():
						tkmb.showerror("Error","Please enter your email!")					
				else:
					if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", entry2.get()):
							tkmb.showerror("Error","Your email is not valid!")
					else:
						mail = entry2.get()
						print mail
						ip = info.split(',')[0]
						file = open('user_info.txt','w') 
						file.write(ip+','+uname+','+mail) 
						file.close()
						tkmb.showinfo("Success","Email saved!")	
			except:
				if not entry1.get():
					tkmb.showerror("Error","Please enter your name!")				
				else:
					if not entry2.get():
						tkmb.showerror("Error","Please enter your email!")					
					else:
						if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", entry2.get()):
							tkmb.showerror("Error","Your email is not valid!")
						else:
							username = entry1.get()
							mail = entry2.get()
							ip = get_ip_address()
							print ip
							print username
							print mail

							file = open('user_info.txt','w') 
							file.write(ip+','+username+','+mail) 
							file.close()
							tkmb.showinfo("Success","Success")		
							print now.strftime("%Y-%m-%d")
				

		def get_ip_address():
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(("8.8.8.8", 80))
			return s.getsockname()[0]


		#def btnSendClicked():
			
		tk.Frame.__init__(self, parent)
		self.controller = controller
		label = tk.Label(self, text="Register", font=controller.title_font)
		label.pack(side="top", fill="x", pady=10)

		frame1 = Frame(self)
		frame1.pack(fill=X)
		lbl1 = Label(frame1, text="Name", width=6, font=controller.label_font)
		lbl1.pack(side=LEFT, padx=5, pady=5)
  
		file = open('user_info.txt', 'r') 
		info = file.read() 
		
		uname = info.split(',')[1]
		if not uname:
			entry1 = Entry(frame1, font=18)
			entry1.pack(fill=X, padx=15, expand=True)
		else:			
			entry1 = Entry(frame1, font=18)
			entry1.pack(fill=X, padx=15, expand=True)
			entry1.insert(END, uname)
			entry1.config(state="disabled")

		frame2 = Frame(self)
		frame2.pack(fill=X)
  
		lbl2 = Label(frame2, text="Email", width=6, font=controller.label_font)
		lbl2.pack(side=LEFT, padx=5, pady=5)
		entry2 = Entry(frame2, font=18)
		entry2.pack(fill=X, padx=15, expand=True)

		btnSave = tk.Button(self, text="Save", command=btnSaveClicked, font=controller.button_font)
		btnSave.pack()
		
		#btnSend = tk.Button(self, text="Send", command=btnSendClicked, font=controller.button_font)
		#btnSend.pack()
		
		lb5 = Label(self, text="\n\n")
		lb5.pack()	
		
		button = tk.Button(self, text="Go back to Home page", command=lambda: controller.show_frame("HomePage"), font=controller.button_font)
		button.pack()
		
class Capture(tk.Frame):

	def __init__(self, parent, controller):

		global quit_walking
		quit_walking = Event()
		q = Queue.Queue()

		def btnStartWithoutSnortClicked():
			btnStartWithoutSnort.config(state='disabled')
			btnStartWithSnort.config(state='disabled')
			btnStop.config(state='normal')

			alan = Thread(target=walkerLoop)
			alan.start()


		def walkerLoop():
			global quit_walking
			while not quit_walking.is_set():
				cap = sniff(count=100,timeout=50,iface='ens33')
				q.put(cap)
				a = q.get()
				wrpcap('sniff.pcap', a)

			quit_walking = Event()

		def checkPcap():
			print os.path.isfile('aa.pcap')


		def btnStartWithSnortClicked():
			btnStartWithoutSnort.config(state='disabled')
			btnStartWithSnort.config(state='disabled')
			btnStop.config(state='normal')

			pid = run.runSnort()
			btnStartWithoutSnortClicked()

		
			
		def btnStopClicked():
			btnStartWithoutSnort.config(state='normal')
			btnStartWithSnort.config(state='normal')
			btnStop.config(state='disabled')

			try:
				run.stopSnort()
				print 's'
			except:
				print 'ns'

			global quit_walking
			quit_walking.set()
			
		
		def isUsingSnort():
			file = open('usingSnort.txt','w') 
			file.write(str(v.get())) 
			file.close()


		def btnRunBroClicked():
			import runbro as rb
			rb.exportListFile()
			rb.sortListFile()
		
		def btnCheckFileClicked():
			print os.path.isfile('aa.pcap')



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
		self.rowconfigure(5, pad=0, weight=1)
		self.rowconfigure(6, pad=0, weight=1)


		label = tk.Label(self, text="Capture", font=controller.title_font)
		label.grid(row=0, columnspan=4, sticky=NSEW)
		
		btnHome = tk.Button(self, text="Go back to Home page",
	                           command=lambda: controller.show_frame("HomePage"), font=controller.button_font)
		btnHome.grid(row=6, columnspan=4)


		v = tk.IntVar()

		btnStartWithSnort = tk.Button(self, text="Start", command=btnStartWithSnortClicked, width=15, font=controller.button_font, fg='green')
		btnStartWithSnort.grid(row=1, column=0)
		btnStartWithSnort.config(font='Arial 14 bold')
		
		btnStartWithoutSnort = tk.Button(self, text="Start Without Snort", width=15, command=btnStartWithoutSnortClicked, font=controller.button_font, fg='green')
		btnStartWithoutSnort.grid(row=1, column=1)
		btnStartWithoutSnort.config(font='Arial 14 bold')

		btnStop = tk.Button(self, text="Stop", command=btnStopClicked, width=15, font=controller.button_font, fg='red')
		btnStop.grid(row=1, column=3)
		btnStop.config(state='disabled', font='Arial 14 bold')

#		btnCheckFile = tk.Button(self, text="Check File", command=btnCheckFileClicked, width=15, font=controller.button_font)
#		btnCheckFile.grid(row=3, columnspan=4)		

#		label = tk.Label(self, text="\n", font=controller.title_font)
#		label.grid(row=2, columnspan=4, sticky=NSEW)

		tcptitle = tk.Label(self, text="TCP PACKETS", font=15)
		tcptitle.grid(row=3, column=0)
		udptitle = tk.Label(self, text="UDP PACKETS", font=15)
		udptitle.grid(row=3, column=1)
		icmptitle = tk.Label(self, text="ICMP PACKETS", font=15)
		icmptitle.grid(row=3, column=2)
		totaltitle = tk.Label(self, text="TOTAL", font=15, fg='blue')
		totaltitle.grid(row=3, column=3)

		tcp = tk.Label(self, text="0", font=15)
		tcp.grid(row=4, column=0)
		udp = tk.Label(self, text="0", font=15)
		udp.grid(row=4, column=1)
		icmp = tk.Label(self, text="0", font=15)
		icmp.grid(row=4, column=2)
		total = tk.Label(self, text="0", font=15, fg='blue')
		total.grid(row=4, column=3) 		
		
		label = tk.Label(self, text="\n\n\n\n\n", font=controller.title_font)
		label.grid(row=5, columnspan=4, sticky=NSEW)

class Graph(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text="Graph", font=controller.title_font)
	        label.pack(side="top", fill="x", pady=10)
	        button = tk.Button(self, text="Go back to Home page",
	                           command=lambda: controller.show_frame("HomePage"), font=controller.button_font)
	        button.pack()

class About(tk.Frame):

	def __init__(self, parent, controller):
	        tk.Frame.__init__(self, parent)
	        self.controller = controller
	        label = tk.Label(self, text="About", font=controller.title_font)
	        label.pack(pady=10)

		lbInfo = tk.Label(self, text="IDS Tool is an desktop application built by: ...\nVisit our website at: www.idstool.com\n", font=controller.label_font)
		lbInfo.config(justify=LEFT)
		lbInfo.pack()

	        button = tk.Button(self, text="Go back to Home page",
	                           command=lambda: controller.show_frame("HomePage"), font=controller.button_font)
	        button.pack()
		
	
if __name__ == "__main__":

	app = SampleApp()
	app.geometry("750x500")
	app.title("Supa IDS")
		
	def on_closing():
		try:
			run.stopSnort()
			print 'snort'
			app.destroy()
		except: 
			print 'no snort'
			app.destroy()
			

	app.protocol("WM_DELETE_WINDOW", on_closing)

	app.mainloop()
