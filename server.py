import socket,time,msgpack
from   datetime import datetime
import collections
UDP_IP = ""
UDP_PORT = 1723
Buffer_size=1024
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))
s_cr_time=0
s_st_time=0
D1=s_cr_time-s_st_time
i=0
real_max=0
real_min= 0
all_jitter=[]
filename = "UDP_JITTER " + datetime.now().strftime("%m-%d-%H-%M-%S")
filename1 = "UDP_LOSS " + datetime.now().strftime("%m-%d-%H-%M-%S")
save_path="c:/users/admin/Desktop/jitter/%s.csv"
appendfile = open(save_path % filename, "a")
appendfile_l=open(save_path % filename1, "a")
info_config= str("IP , PORT")
appendfile.write(info_config+',')
appendfile_l.write(info_config+',')
info_config= str("average code length")
appendfile.write(info_config+',')
appendfile_l.write(info_config+',')
info_config= str('approximate period between packets')
appendfile.write(str(info_config)+'\n')
appendfile_l.write(str(info_config)+'\n')
info_config= str([UDP_IP , UDP_PORT])
appendfile.write(info_config+',')
appendfile_l.write(info_config+',')
data, addr = sock.recvfrom(Buffer_size)
# info_config=data.decode()
# info_config=str(len(str(MESSAGE)))
appendfile.write(info_config+',')
appendfile_l.write(info_config+',')
# info_config=str(sleep)
# appendfile.write(str(info_config)+'\n')
# appendfile_l.write(str(info_config)+'\n')
flag=True
while True:
       data, addr = sock.recvfrom(Buffer_size) # buffer size is 1024 bytes
       data = msgpack.unpackb(data,use_list=False)
       if flag :
            # frst_seq= int(data.decode().split("'")[1])-1
            frst_seq=(data)[1]
            flag=False
       # print ("received message:", data.decode())
       print("received message:" , data.decode())
       cr_time=datetime.now().strftime("%H:%M:%S.%f")
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
       #
       #
