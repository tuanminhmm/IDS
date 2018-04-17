import subprocess
import os


def bro():
	subprocess.Popen("/usr/local/bro/bin/bro -r sniff.pcap darpa2gurekddcup.bro > conn.list", shell=True, stdout=subprocess.PIPE).stdout.read()

def sort():
	subprocess.Popen("sort -n conn.list > conn_sort.list", shell=True, stdout=subprocess.PIPE).stdout.read()

def exportFile():
	subprocess.Popen("./trafAld.out conn_sort.list", shell=True, stdout=subprocess.PIPE).stdout.read()
