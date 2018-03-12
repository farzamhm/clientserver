import socket
import time,datetime,random,math
import msgpack
UDP_IP = "127.0.0.1"
UDP_PORT = 1723
MESSAGE = "Hello, World!"
LINK_LOSS=1
sleep=0.4
sock = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)  # UDP
seq=1
sock.sendto( str(0.4).encode(), (UDP_IP, UDP_PORT))
while 1:
    # TP_MESSAGE =str(['{0:08}'.format(seq),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),MESSAGE])
    TP_MESSAGE = str(['{0:08}'.format(seq) , datetime.datetime.now().strftime("%H:%M:%S.%f"), MESSAGE])
    B_TP_MESSAGE=msgpack.packb(TP_MESSAGE,use_bin_type=True)
    if math.floor(random.uniform(0,1)+LINK_LOSS):
        # sock.sendto(TP_MESSAGE.encode(), (UDP_IP, UDP_PORT))
        sock.sendto(B_TP_MESSAGE, (UDP_IP , UDP_PORT))
        # print(B_TP_MESSAGE)
        # print(UDP_IP,UDP_PORT)
    time.sleep(sleep)
    # time.sleep(abs(random.gauss(0,0.2))) #Jitter as normal distribution
    seq +=1