import socket
import threading

socket_client = socket.socket()        
ip_addr = '127.0.0.1'
port = 12345
socket_client.connect((ip_addr, port))
socket_client.send('robot1krsbipolibankerenjos'.encode())
socket_client.send('halo1'.encode())
socket_client.send('halo2'.encode())

disconnect = False

def socket_conn():
    global socket_client
    global port
    socket_client.connect(('127.0.0.1', port))
    socket_client.send('robot1krsbipolibankerenjos'.encode())

def receive():
    global socket_client
    global disconnect
    while True:
        print (socket_client.recv(1024).decode())
        if disconnect:
            socket_client.close()
            break

def close_conn():
    global disconnect
    disconnect = False

def send_data():
    global socket_client
    global disconnect
    while True:
        s = input()
        if s == 'quit':
            disconnect = False
            
        elif s == 'conn':
            socket_conn()
        else:
            socket_client.send('halo'.encode())
            print(f'sent: {s}')

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=send_data)

t1.start()
t2.start()
t1.join()
t2.join()
print("Done!")