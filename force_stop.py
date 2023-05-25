def socket_client():
    import socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))
    client.send(f'force stop'.encode())
    from_server = client.recv(4096).decode('utf8')
    print(from_server)
    if from_server=='force stop':
        print('uwauwauwa')
    client.close()

socket_client()