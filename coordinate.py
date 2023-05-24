from flask import Flask
import socket
import pyautogui
import math
import requests

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

@app.route('/start')
def start_server():
    try:
        requests.get('http://127.0.0.1:5000/mouse',verify=False, timeout=0.1)
    except:
        pass
    return 'ok'

@app.route('/mouse')
def mouse():
    mouse_service()
    return 'ok'
        
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
        x_fix, y_fix = x/point_per_m*100, -y*point_per_m*100

        positionStr = 'X: ' + str(x_fix).rjust(4) + ' Y: ' + str(y_fix).rjust(4)
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
    