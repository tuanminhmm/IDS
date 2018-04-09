import subprocess
import os
from subprocess import call

def exportListFile():
	#bro_process = subprocess.Popen(['/usr/local/bro/bin/bro', '-r', 'cap.pcap', 'darpa2gurekddcup.bro', '>', 'conn.list'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, close_fds=True)
	#call(["/usr/local/bro/bin/bro", "-r", "cap.pcap", "darpa2gurekddcup.bro", ">", "conn.list"])
	subprocess.Popen("/usr/local/bro/bin/bro -r cap.pcap darpa2gurekddcup.bro > conn.list", shell=True, stdout=subprocess.PIPE).stdout.read()
	#subprocess.Popen("ls -l", shell=True, stdout=subprocess.PIPE).stdout.read()

def sortListFile():
	subprocess.Popen("sort -n list/conn.list > conn_sort.list", shell=True, stdout=subprocess.PIPE).stdout.read()

