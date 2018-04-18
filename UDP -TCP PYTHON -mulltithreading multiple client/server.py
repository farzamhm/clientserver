import socket,time,msgpack
import random
import threading
from   datetime import datetime
import collections
import math
import sys
import traceback
from threading import Thread

UDP_IP = ""
UDP_PORT = 5010
Buffer_size = 1024
TCP_IP = ''
TCP_PORT = 80
BUFFER_SIZE = 1024
event=threading.Event()

def udp_connection_reciver():

    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
    print("Server UDP socket created")
    s_cr_time=0
    s_st_time=0
    D1=s_cr_time-s_st_time
    i=0
    real_max=0
    real_min= 0
    all_jitter=[]
    # filename = "UDP_JITTER " + datetime.now().strftime("%m-%d-%H-%M-%S")
    # filename1 = "UDP_LOSS " + datetime.now().strftime("%m-%d-%H-%M-%S")
    # save_path="c:/users/admin/Desktop/jitter/%s.csv"
    # appendfile = open(save_path % filename, "a")
    # appendfile_l=open(save_path % filename1, "a")
    # info_config= str("IP , PORT")
    # appendfile.write(info_config+',')
    # appendfile_l.write(info_config+',')
    # info_config= str("average code length")
    # appendfile.write(info_config+',')
    # appendfile_l.write(info_config+',')
    # info_config= str('approximate period between packets')
    # appendfile.write(str(info_config)+'\n')
    # appendfile_l.write(str(info_config)+'\n')
    # info_config= str([UDP_IP , UDP_PORT])
    # appendfile.write(info_config+',')
    # appendfile_l.write(info_config+',')
    # data, addr = sock.recvfrom(Buffer_size)
    # # info_config=data.decode()
    # # info_config=str(len(str(MESSAGE)))
    # appendfile.write(info_config+',')
    # appendfile_l.write(info_config+',')
    # info_config=str(sleep)
    # appendfile.write(str(info_config)+'\n')
    # appendfile_l.write(str(info_config)+'\n')
    flag=True
    while True:
            try:
               data, addr = sock.recvfrom(Buffer_size) # buffer size is 1024 bytes
               data = msgpack.unpackb(data,use_list=False)
               if flag :
                    # frst_seq= int(data.decode().split("'")[1])-1
                    frst_seq=(data)[1]
                    flag=False
               # print ("received message:", data.decode())
               print("received message:" , data.decode())
               # print("UDP: ", addr)
               cr_time=datetime.now().strftime("%H:%M:%S.%f")
               servercmd = msgpack.packb("i received"+ str(addr),use_bin_type=True)

               sock.sendto(servercmd, addr)
               #####################################################################

               # s_st_time =float(data.decode().split("',")[1].split(':')[2])
               # s_cr_time=float(cr_time.split(':')[2])
               # D2=s_cr_time-s_st_time
               # recv_seq=int(data.decode().split("'")[1])
               # if recv_seq !=frst_seq+1 :
               #     real_max =0
               #     real_min =0
               #     frst_seq= recv_seq-1
               #     print('LOSSSSSSSSSSSSSSSSSSSSSSSSSSS')
               #     appendfile_l = open(save_path % filename1, "a")
               #     appendfile_l.write(str(D2 - D1) + '\n')
               #     # appendfile_l.close()
               #
               # real_max=max(abs(D2-D1),real_max)
               # real_min=min(abs(D2-D1),real_min)
               # appendfile=open(save_path %filename,'a')
               # appendfile.write(str(D2-D1)+'\n')
               # # appendfile.close()
               # D1=D2
               # print("received time:" , cr_time)
               # print(s_cr_time,s_st_time,"seq:",frst_seq,"D2:",D2)
               # # i=1
               # frst_seq+=1
               # print ( str(addr))
            except msgpack.exceptions.ExtraData:
                print("a new Connection started!")
                data , addr = sock.recvfrom(Buffer_size)  # buffer size is 1024 bytes
                data = msgpack.unpackb(data , use_list=False)
                print("received message:" , data.decode() , addr)
                servercmd = msgpack.packb("i received it" , use_bin_type=True)
                sock.sendto(servercmd , addr)

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
            traceback.print_exc()  ######################?????????????????????????????????????????????????s

    soc.close()

def client_thread(connection , ip , port , max_buffer_size=5120):
    is_active = True
    seq = 1
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


