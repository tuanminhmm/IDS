import subprocess
import os

#global snort_process	
def runSnort():
	global snort_process 
	#echo = subprocess.Popen(['echo','123qwe!@#'],stdout=subprocess.PIPE)
	#os.system('sudo su')
	#os.system('123qwe!@#')
	snort_process = subprocess.Popen(['snort', '-i', 'ens33', '-A', 'fast', '-c', '/etc/snort/snort.conf'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,universal_newlines=True, close_fds=True)
	#sudo_prompt = snort_process.communicate('123qwe!@#' + '\n')
	print snort_process.pid
	#print os.popen("snort -i ens33 -A fast -c /etc/snort/snort.conf", 'w').getpid

	#os.popen("sudo snort -i ens33 -A fast -c /etc/snort/snort.conf", 'w').write("123qwe!@#")
	#os.system('pgrep -f "sudo snort -i ens33 -A fast -c"')



def stopSnort():
	snort_process.kill()
	

	#snort_process = subprocess.Popen(['sudo', 'snort', '-i', 'ens33', '-A', 'fast', '-c', '/etc/snort/snort.conf'],stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,universal_newlines=True, close_fds=True)
	#subprocess.call("exit 1", shell=True)
	#subprocess.Popen.terminate(snort_process)
	#subprocess.Popen('sudo service stop snort' , shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,universal_newlines=True, close_fds=True).write('123qwe!@#')
	#subprocess.Popen('123qwe!@#', shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1,universal_newlines=True, close_fds=True)
	#subprocess.Popen.kill(snort_process)
	#snort_process.kill()

	#os.popen("sudo systemctl diabled", 'w').write("123qwe!@#")
