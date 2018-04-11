import socket,time,msgpack
import random
import threading
from   datetime import datetime
import collections
import math

UDP_IP = ""
UDP_PORT = 5010
Buffer_size = 1024
TCP_IP = ''
TCP_PORT = 80
BUFFER_SIZE = 1024
event=threading.Event()
# addr_tcp=[]
# def init_connection():
#     while True:
#         print("initiation")
#         sock_tcp = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
#         sock_tcp.bind((TCP_IP , TCP_PORT))
#         sock_tcp.listen(2)
#         conn_tcp , addr_tcp = sock_tcp.accept()
#         print('One TCP Connection Created from:' , addr_tcp)
#         event.set()
#         time.sleep(5)
def udp_connection_reciver():
    # event.wait()
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))
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
               print(addr)
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

def tcp_connection_sender():
    # event.wait()
    sock_tcp = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    sock_tcp.bind((TCP_IP , TCP_PORT))
    sock_tcp.listen(2)
    conn_tcp , addr_tcp = sock_tcp.accept()
    print('One TCP Connection Created from:' , addr_tcp)
    LINK_LOSS = 0.1
    sleep = 2
    seq_tcp=1
    # global addr_tcp
    while True:
        if math.floor(random.uniform(0 , 1) + LINK_LOSS):

            TCP_MESSAGE ="Message: "+str(seq_tcp) +" from server over TCP to "  +"at: "+ str(datetime.now().strftime("%H:%M:%S.%f"))
            B_TCP_MESSAGE = msgpack.packb(TCP_MESSAGE , use_bin_type=True)
            conn_tcp.send(B_TCP_MESSAGE)
            seq_tcp+=1
        print("server tcp working")
        time.sleep(sleep)

# init_thread=threading.Thread(target=init_connection)
udp_thread=threading.Thread(target=udp_connection_reciver,name= 'udp_thread')
tcp_thread = threading.Thread(target=tcp_connection_sender ,name='tcp_thread', daemon=True)

# init_thread.start()
udp_thread.start()
tcp_thread.start()

# init_thread.join()
udp_thread.join()
tcp_thread.join()

print('our ending value of total is' )
# if __name__ == "__main__":
#     udp_connection_reciver()


