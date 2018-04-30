import socket,time,msgpack
import random
import threading
from   datetime import datetime
import collections
import math
import sys
import traceback
from threading import Thread
import os
from udp_measure import UdpJitterStat

UDP_IP = ""
UDP_PORT = 5010
Buffer_size = 1024
TCP_IP = ''
TCP_PORT = 80
BUFFER_SIZE = 1024
event=threading.Event()
sleep=0
jittr_lst=[]
jj=1
jitt=dict()
MESSAGE="Hello,server World!"
def udp_connection_reciver():

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    print("Server UDP socket created")

    while True:
            try:
               data, addr = sock.recvfrom(Buffer_size) # buffer size is 1024 bytes
               data = msgpack.unpackb(data,use_list=False)
               for i in jittr_lst:
                   # print("hi")
                   if  i[0]==addr[1]:
                       # print("hi2")
                       i[1].run(data)
               print("received message:" , data.decode())

            except msgpack.exceptions.ExtraData:
                print("a new Connection started!")
                data , addr = sock.recvfrom(Buffer_size)  # buffer size is 1024 bytes
                data = msgpack.unpackb(data , use_list=False)
                ###################instantiate jitter and  packet loss#######################
                obj_name=str(addr[1])
                vars()[obj_name]=UdpJitterStat(addr[0],addr[1])

                jittr_lst.append([addr[1],vars()[obj_name]])
                # jittr[obj_jtt_name] = UdpJitterMeasure(UDP_IP , UDP_PORT)
                print("received message:" , data.decode() , addr)

def start_tcp_server():

    soc = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR ,1)  # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire

    print("Server TCP Socket created")
    try:
        soc.bind((TCP_IP , TCP_PORT))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(5)  # queue up to 5 requests

    # infinite loop- do not reset for every requests
    while True:
        connection , address = soc.accept()
        ip , port = str(address[0]) , str(address[1])
        print("TCP Connection with " + ip + ":" + port)

        try:
            Thread(target=client_thread , args=(connection , ip , port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()  ######################?????????

    soc.close()

def client_thread(connection , ip , port , max_buffer_size=5120):
    is_active = True
    seq = 1
###################################################tcp connection testing#####################################
    filename="TCP_delaytest_serverside "+str(ip)+" "+str(port)+" "+ datetime.now().strftime("%m-%d-%H-%M-%S")
    save_path = os.path.realpath(os.path.join(os.getcwd() , os.path.dirname(filename))).replace("\\" , "/") + "/%s.csv"
    appendfile = open(save_path % filename , "a")
    appendfile.write(("Round Trip Delay" + "," + "Average Round Trip Delay") + '\n')
    ave_delay = 0
    for i in range(100):
        data = connection.recv(BUFFER_SIZE)
        connection.send(data)
    for i in range(100):
        TP_MESSAGE = str(['99999999' , datetime.now().strftime("%H:%M:%S.%f") , MESSAGE])
        B_TP_MESSAGE = msgpack.packb(TP_MESSAGE , use_bin_type=True)
        connection.send((B_TP_MESSAGE))
        data = connection.recv(BUFFER_SIZE)
        data = msgpack.unpackb(data )
        rcv_time = float(datetime.now().strftime("%H:%M:%S.%f").split(':')[2])
        s_st_time = float(data.decode().split("',")[1].split(':')[2])
        # s_st_time = float(data[1].split(':')[2])
        # seq += 1
        ave_delay = ((rcv_time - s_st_time) + ave_delay * i) / (i + 1)
        appendfile = open(save_path % filename , "a")
        # appendfile.write(str(rcv_time - s_st_time) + '\n')
        appendfile.write((str(rcv_time - s_st_time) + "," + str(ave_delay)) + '\n')
    appendfile.close()
############################################end tcp connection testing#################################################
    while is_active:
        msg_2_client = 'hello ' + str(seq) + " to: " + str(ip) + " " + str(port) + " at: " + str(time.time())

        print("sending: ",msg_2_client)
        connection.send(msg_2_client.encode())
        time.sleep(2)
        seq += 1

udp_thread=threading.Thread(target=udp_connection_reciver,name= 'udp_thread')
udp_thread.start()



if __name__ == "__main__":
     start_tcp_server()


