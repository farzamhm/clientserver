#!/usr/bin/env python
import socket
import msgpack
TCP_IP = ''
TCP_PORT = 8000
BUFFER_SIZE =1024
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.bind((TCP_IP , TCP_PORT))
s.listen(1)
conn , addr = s.accept()
print('Connection address:' , addr)
i=1
while 1:
    data = conn.recv(BUFFER_SIZE)
    data = msgpack.unpackb(data,raw=False)
    if not data: break
    print("received data:" , data)
    servermsg=msgpack.packb(data,use_bin_type=True)
    # conn.send(str(servermsg).encode())  # echo
    conn.send(servermsg)
    i+=1
conn.close()