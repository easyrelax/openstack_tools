from socket import *
import socket 
import sys

msg = sys.argv[1]
ip_port=("127.0.0.1",8000)
back_log =1
buffer_size = 1024
 
tcp_client = socket.create_connection(ip_port, 1)
tcp_client.sendall(msg.encode("utf-8"))
data = tcp_client.recv(buffer_size)
print("Server deal the data:", data.decode("utf-8"))
tcp_client.close()
