#import pyshark
#import os

from scapy.all import *

Cap = sniff(count=100,timeout=50,iface='ens33')





#def abc():


#try:
#	os.remove('cap.pcap')
#	print 'ok'
#except:
#	print 'no'
#cap = pyshark.LiveCapture(interface='ens33')
#cap.sniff(timeout=20)
#return cap






# no - time - src - des - protocol - length - info
#	time = cap[0].frame_info.time_relative
#print cap

#	try:
#		ip_src = cap[0].ip.src
#	except AttributeError:
#		ip_src = 'null'

#	try:
#		ip_dst = cap[0].ip.dst
#	except AttributeError:
#		ip_dst = 'null'
#

	#i = 0
	#tcp = 0
	#udp = 0
	#icmp = 0
	#total = 0

	#while i < 10:
	#	protocol = cap[i].highest_layer
	#	print protocol
	#	i+=1

	#	if protocol == 'TCP':
	#		tcp += 1
	#	if protocol == 'UDP':
	#		udp += 1
	#	if protocol == 'ICMP':
	#		icmp += 1

	#total = tcp + udp + icmp

	#return [tcp, udp, icmp, total]

#	if protocol == 'TCP':
#		return 1
#	else:
#		if protocol == 'UDP':
#			return 2
#		else:
#			if protocol == 'ICMP':
#				return 3
	
	#length = cap[0].length

				
#	lbPacket = tk.Label(self, text="|"+str(i+1)+" "*(3-len(str(i+1)))+"| "+cap[i].frame_info.time_relative+" | "+ip_src+" "*(16-len(str(ip_src)))+"| "+ip_dst+" "*(16-len(str(ip_dst)))+"| "+cap[i].highest_layer+" "*(9-len(str(cap[i].highest_layer)))+"| "+cap[i].length+" "*(7-len(str(cap[i].length)))+"| ")
#	lbPacket.pack()
	
