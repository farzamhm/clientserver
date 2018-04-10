#!/usr/bin/env python
import socket
import time
from datetime import datetime
import msgpack
import random
TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 1024
# MESSAGE = "Hello, World!"
MESSAGE=[random.random()*1000,random.random()*1000,random.random()*1000,random.random()*1000,random.random()*1000,random.random()*1000]
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((TCP_IP,TCP_PORT))
seq=1
sleep=1
filename = "TCP_delay " + datetime.now().strftime("%m-%d-%H-%M-%S")
save_path="c:/users/admin/Desktop/delay/%s.csv"
appendfile = open(save_path % filename , "a")
info_config= str("IP , PORT")
appendfile.write(info_config+',')
info_config= str("average code length")
appendfile.write(info_config+',')
info_config= str('sleep time')
appendfile.write(str(info_config)+'\n')
info_config= str([TCP_IP , TCP_PORT])
appendfile.write(info_config+',')
info_config=str(len(str(MESSAGE)))
appendfile.write(info_config+',')
info_config=str(sleep)
appendfile.write(str(info_config)+'\n')
while 1 :
    # TP_MESSAGE = str(['{0:08}'.format(seq) , datetime.datetime.now().strftime("%H:%M:%S.%f"), MESSAGE])
    TP_MESSAGE = ['{0:08}'.format(seq) , datetime.now().strftime("%H:%M:%S.%f") , MESSAGE]
    MESSAGE = [random.random() * 1000 , random.random() * 1000 , random.random() * 1000 , random.random() * 1000 ,
               random.random() * 1000 , random.random() * 1000]
    B_TP_MESSAGE=msgpack.packb(TP_MESSAGE,use_bin_type=True)
    s.sendto((B_TP_MESSAGE) ,(TCP_IP , TCP_PORT))
    data = s.recv(BUFFER_SIZE)
    data =msgpack.unpackb(data,raw=False)
    rcv_time= float(datetime.now().strftime("%H:%M:%S.%f").split(':')[2])
    # s_st_time = float(data.decode().split("',")[1].split(':')[2])
    s_st_time =float( data[1].split(':')[2])
    seq+=1
    appendfile = open(save_path % filename, "a")
    appendfile.write(str(rcv_time-s_st_time)+'\n')
    print(data, rcv_time - s_st_time)
    # print(data.decode())
    time.sleep(sleep)


s.close()