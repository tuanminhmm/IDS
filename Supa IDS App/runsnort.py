import subprocess
import os

def runSnort():
	global snort_process 

	snort_process = subprocess.Popen(['snort', '-i', 'ens33', '-A', 'fast', '-c', '/etc/snort/snort.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,universal_newlines=True, close_fds=True)

def stopSnort():
	try:
		snort_process.kill()
	except:
		pass
	

