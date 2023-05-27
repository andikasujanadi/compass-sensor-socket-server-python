import socket
import time
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))
client.send(f'robot1'.encode())
while True:
    from_server = client.recv(4096).decode('utf8')
    if len(from_server)>0:
        print(f'>>> {from_server}')
