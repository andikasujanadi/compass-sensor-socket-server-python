from flask import Flask
import socket
import pyautogui
import math

app = Flask(__name__)

server = socket.socket()
print ("Socket successfully created")
ip_addr = '127.0.0.1'
port = 12345
angle = 0

max_client = 3
clients = []
for i in range(max_client):
    clients.append(None)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/robot<int:x>/<int:r>')
def robot(x,r):
    global angle
    if x==1:
        angle = r
    if clients[x]:
        try:
            clients[x].send(toByte(str(r)))
            return f'Robot {x} {r} deg\n{clients[x]}' 
        except:
            clients[x]=None
    return f'hmmm?'

@app.route('/clients')
def count_clients():
    global clients
    sum = 0
    for i in clients:
        if i:
            sum+=1
    return f'{sum} client(s) connected right now'

@app.route('/server')
def serverku():
    main()
    return 'ok'

@app.route('/mouse')
def mouse():
    mouse_service()
    return 'ok'

def main():
    global clients
    global max_client
    loop = True
    server.bind(('', port))        
    print ("socket binded to %s" %(port))
    
    server.listen(5)    
    print ("socket is listening")
    
    while loop:
        c, addr = server.accept()
        print ('Got connection from', addr )
        fingerprint = c.recv(1024).decode()
        print(f'in >>> {fingerprint}')
        if arr_in_str(['robot','krsbipolibankerenjos'], fingerprint):
            id = -1
            try:
                id = int(fingerprint[5])
            except:
                id = -1
            if id >=0 and id<=max_client and not clients[id]:
                c.send(f'Connected to KRSBI-B Poliban Server, welcome Robot {id}'.encode())
                clients[id] = c
                print(f'robot {id} initialize')
            else:
                c.send(toByte(f'you cannot connect to this server, robot {id} already initialize'))
        else:
            c.send(f'access denied')
        
def mouse_service():
    global angle
    init_x=960
    init_y=540
    boundary = 200
    x0, y0 = init_x, init_y
    x, y = 0, 0
    x_fix, y_fix = 0, 0
    point_per_m = 1735
    pyautogui.moveTo(init_x, init_y)
    while True:
        x1, y1 = pyautogui.position()
        if x1 < (init_x-boundary):
            pyautogui.moveTo(init_x+boundary, y1)
            x -= (boundary*2+1)*round(math.cos(math.radians(angle)),15)
            y -= (boundary*2+1)*round(math.sin(math.radians(angle)),15)
        elif x1 > (init_x+boundary):
            pyautogui.moveTo(init_x-boundary, y1)
            x += (boundary*2+1)*round(math.cos(math.radians(angle)),15)
            y += (boundary*2+1)*round(math.sin(math.radians(angle)),15)
        if y1 < (init_y-boundary):
            pyautogui.moveTo(x1, init_y+boundary)
            y -= (boundary*2+1)*round(math.cos(math.radians(angle)),15)
            x -= (boundary*2+1)*round(math.sin(math.radians(angle)),15)
        elif y1 > (init_y+boundary):
            pyautogui.moveTo(x1, init_y-boundary)
            y += (boundary*2+1)*round(math.cos(math.radians(angle)),15)
            x += (boundary*2+1)*round(math.sin(math.radians(angle)),15)

        x += (x1 - x0)*round(math.cos(math.radians(angle)),15) + (y1 - y0)*round(math.sin(math.radians(angle)),15)
        y += (y1 - y0)*round(math.cos(math.radians(angle)),15) + (x1 - x0)*round(math.sin(math.radians(angle)),15)
        x_fix, y_fix = x/point_per_m*100, -y/point_per_m*100

        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        
        x0, y0 = x1, y1

def arr_in_str(arr,s):
    for a in arr:
        if a not in s:
            return False
    return True

def toByte(s):
    return s.encode('utf-8')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    