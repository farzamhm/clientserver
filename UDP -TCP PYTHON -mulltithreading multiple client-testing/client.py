import socket
import os
import time,datetime,random,math
import msgpack
import threading
import sys
# UDP_IP = "68..."
UDP_IP = "127.0.0.1"
UDP_PORT = 5010
MESSAGE = "Hello,client World!"
TCP_IP = UDP_IP
TCP_PORT = 80
BUFFER_SIZE = 1024
LINK_LOSS = 1
sleep = 2

def udp_connection():
    sock = socket.socket(socket.AF_INET ,socket.SOCK_DGRAM)
    # sock.bind(("",UDP_PORT))# UDP
    seq=1
    sock.sendto( str(0.4).encode(), (UDP_IP, UDP_PORT))
    while 1:
        # TP_MESSAGE =str(['{0:08}'.format(seq),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),MESSAGE])
        TP_MESSAGE = str(['{0:08}'.format(seq) , datetime.datetime.now().strftime("%H:%M:%S.%f"), MESSAGE])
        B_TP_MESSAGE=msgpack.packb(TP_MESSAGE,use_bin_type=True)
        if math.floor(random.uniform(0,1)+LINK_LOSS):
            # sock.sendto(TP_MESSAGE.encode(), (UDP_IP, UDP_PORT))
            sock.sendto(B_TP_MESSAGE, (UDP_IP , UDP_PORT))
            print("sending:", TP_MESSAGE)
            # print(sock.getsockname())
            # servercmd , add = sock.recvfrom(1024)
            # servercmd=msgpack.unpackb(servercmd,use_list=False)
            # print('Recieved Msg from server: ', servercmd.decode())
            # print('client side info',add)
        time.sleep(sleep)
        # time.sleep(abs(random.gauss(0,0.2))) #Jitter as normal distribution
        seq +=1

def tcp_connection():
    flag=True
    Soc_tcp = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    while flag:
        try:
            Soc_tcp.connect((TCP_IP , TCP_PORT))
            flag=False
        except:

            print("Connection error")

    #################################################tcp connection testing##############################
    filename = "TCP_delaytest_clientside " +str(Soc_tcp.getsockname())+ datetime.datetime.now().strftime("%m-%d-%H-%M-%S")
    save_path = os.path.realpath(os.path.join(os.getcwd() , os.path.dirname(filename))).replace("\\" , "/") + "/%s.csv"
    appendfile = open(save_path % filename , "a")
    appendfile.write(("Round Trip Delay" + "," + "Average Round Trip Delay") + '\n')
    ave_delay=0
    for i in range(100):
        TP_MESSAGE = str(['99999999' , datetime.datetime.now().strftime("%H:%M:%S.%f") , MESSAGE])
        B_TP_MESSAGE = msgpack.packb(TP_MESSAGE , use_bin_type=True)
        Soc_tcp.sendto((B_TP_MESSAGE) , (TCP_IP , TCP_PORT))
        data = Soc_tcp.recv(BUFFER_SIZE)
        data = msgpack.unpackb(data)
        rcv_time = float(datetime.datetime.now().strftime("%H:%M:%S.%f").split(':')[2])
        s_st_time = float(data.decode().split("',")[1].split(':')[2])
        ave_delay=((rcv_time-s_st_time)+ave_delay*i)/(i+1)
        # s_st_time = float(data[1].split(':')[2])

        appendfile = open(save_path % filename , "a")
        appendfile.write((str(rcv_time - s_st_time) +","+ str(ave_delay)) + '\n')
    appendfile.close()
    for i in range (100):
        data = Soc_tcp.recv(BUFFER_SIZE)
        Soc_tcp.sendto(data , (TCP_IP , TCP_PORT))

############################################end tcp connection testing##########################################

    udp_thread.start()
    while True:
        try:
            recv_msg = Soc_tcp.recv(BUFFER_SIZE).decode("utf8")

            print("Recieving:" , recv_msg)

        except:
               print('exception')
               try:
                   Soc_tcp = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                   Soc_tcp.connect((TCP_IP , TCP_PORT))

               except:
                   pass

               pass



udp_thread = threading.Thread(target=udp_connection,name= 'udp_thread')
tcp_thread = threading.Thread(target=tcp_connection ,name='tcp_thread', daemon=True)



tcp_thread.start()

# init_thread.join()
# udp_thread.join()
tcp_thread.join()

udp_thread.start()

print('program finished')
# if __name__ == "__main__":
#     udp_connection()
