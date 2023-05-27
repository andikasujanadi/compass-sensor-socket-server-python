def socket_server():
    import socket
    clients = []
    robot1= None
    robot2= None
    sensor1= None
    sensor2= None
    fc= None
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(('127.0.0.1', 12345))
    serv.listen(5)

    while True:
        conn, addr = serv.accept()
        data = conn.recv(4096)
        from_client = data.decode('utf8')
        print(f'{addr}{from_client}')
        if conn not in clients:
            if 'robot1' in from_client:
                robot1 = conn
                clients.append(conn)
                print('robot 1 connected')
            elif 'robot2' in from_client:
                robot2 = conn
                clients.append(conn)
                print('robot 2 connected')
            elif 'sensor1' in from_client:
                sensor1 = conn
                clients.append(conn)
                # sensor1.send('ok'.encode('utf8'))
                print('sensor 1 connected')
            elif 'sensor2' in from_client:
                sensor2 = conn
                clients.append(conn)
                # sensor1.send('ok'.encode('utf8'))
                print('sensor 2 connected')

        if 'init_fc' in from_client:
            if sensor1:sensor1.send('init_fc'.encode('utf8'))
            if sensor2:sensor2.send('init_fc'.encode('utf8'))
            print('force close triggered')
    
        # if 'R1' in from_client and sensor1: 
        #     print('okeeeeee')
        #     sensor1.send('sensor 1 ok'.encode('utf8'))
        # if 'R2' in from_client and sensor2: 
        #     sensor2.send('sensor 2 ok'.encode('utf8'))
    print ('client disconnected and shutdown')

socket_server()