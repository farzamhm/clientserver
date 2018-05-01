import sys
import subprocess 
def wireless_stat():
	res=subprocess.call(['iw','dev','wlan0', 'station', 'dump', '-v '])
	print(res)
wireless_stat()
