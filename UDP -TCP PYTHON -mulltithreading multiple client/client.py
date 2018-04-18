import socket
import time,datetime,random,math
import msgpack
import threading
import sys
# UDP_IP = "68.182.134.78"
UDP_IP = "127.0.0.1"
UDP_PORT = 5010
MESSAGE = "Hello, World!"
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
    Soc_tcp = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

    try:
        Soc_tcp.connect((TCP_IP , TCP_PORT))
    except:

        print("Connection error")
        sys.exit()

    while True:
        recv_msg = Soc_tcp.recv(1024).decode("utf8")
        if recv_msg == "-":
            pass  # null operation
        print("Recieving:",recv_msg)

udp_thread = threading.Thread(target=udp_connection,name= 'udp_thread')
tcp_thread = threading.Thread(target=tcp_connection ,name='tcp_thread', daemon=True)

# init_thread.start()
udp_thread.start()
tcp_thread.start()

# init_thread.join()
udp_thread.join()
tcp_thread.join()

print('program finished')
# if __name__ == "__main__":
#     udp_connection()