def socket_server():
  import socket
  serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  serv.bind(('127.0.0.1', 12345))
  serv.listen(5)
  while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
      data = conn.recv(4096)
      if not data: break
      from_client = data.decode('utf8')
      print (f'{addr} {from_client}')
      conn.send(f'{from_client}'.encode('utf8'))
    conn.close()
    # break
  print ('client disconnected and shutdown')

socket_server()