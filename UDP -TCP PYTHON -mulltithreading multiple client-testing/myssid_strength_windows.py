import subprocess
def wireless_ssid_win():
        results=subprocess.check_output(["netsh", "wlan", "show", "interfaces"])
        results = results.decode("ascii") # needed in python 3
        results = results.replace("\r","")
        ls = results.split("\n")
        lst=[]
        for i in ls:
            if "SSID" in i:
                print(i)
                lst.append(i)
            if  "Signal" in i:
                print (i)
                lst.append(i)

if __name__ == "__main__":
    wireless_ssid_win()

