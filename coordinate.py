from flask import Flask
import socket
import pyautogui
import math
import requests
import threading

app = Flask(__name__)
use_socket = False

if use_socket:
    socket_client = socket.socket()
    ip_addr = '127.0.0.1'
    port = 12345
    socket_client.connect((ip_addr, port))
    print ("Conected to the server")
angle = 0
robot_id = 0

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/robot<int:x>/<int:r>')
def robot(x,r):
    global robot_id
    global angle
    robot_id = x
    angle = r
    return f'angle'

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
    print('mouse service is on!')
    global robot_id
    global angle
    if use_socket:
        global socket_client

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

        positionStr = 'X: ' + to3d(x_fix).rjust(4) + ' Y: ' + to3d(y_fix).rjust(4)
        if 0:
            print(positionStr, end='')
            print('\b' * len(positionStr), end='', flush=True)
        
        x0, y0 = x1, y1

        if robot_id != 0:
            output = f'R{robot_id}{to3d(angle)}{"-" if x_fix<0 else "+"}{to3d(x_fix)}{"-" if y_fix<0 else "+"}{to3d(y_fix)}'
            print(output, end='')
            print('\b' * len(output), end='', flush=True)
            if use_socket:
                socket_client.send(output.encode())
            pass

def to3d(number):
    if number<0:
        number*=-1
    value = str(int(number))
    if len(value)==3:
        return value
    if len(value)==2:
        return f'0{value}'
    if len(value)==1:
        return f'00{value}'
    return f'asd{value}'

if __name__ == '__main__':
    t1 = threading.Thread(target=start_server)
    t1.start()
    t1.join()
    app.run(debug=True, host='0.0.0.0', port=5000)
    