from flask import Flask
import threading

app = Flask(__name__)

angle = 0
robot_id = 0
for_socket = ''
loop = True

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

def socket_client():
    import socket
    global loop
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 12345))
    print('socket client is on!')
    last_data = ''
    while loop:
        if len(for_socket)>0 and for_socket != last_data:
            client.send(f'{for_socket}'.encode())
            from_server = client.recv(4096)
            print (from_server.decode())
            if from_server=='force stop':
                loop = False
            last_data = for_socket
    client.close()
        
def mouse_service():
    import pyautogui
    import math
    print('mouse service is on!')
    global robot_id
    global angle
    global loop
    global for_socket

    init_x=960
    init_y=540
    boundary = 400
    x0, y0 = init_x, init_y
    x, y = 0, 0
    x_fix, y_fix = 0, 0
    point_per_m = 1735
    pyautogui.moveTo(init_x, init_y)

    while loop:
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

        if True:
            for_socket = f'R{robot_id}{to3d(angle)}{"-" if x_fix<0 else "+"}{to3d(x_fix)}{"-" if y_fix<0 else "+"}{to3d(y_fix)}'
            print(for_socket, end='')
            print('\b' * len(for_socket), end='', flush=True)

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
    try:
        t1 = threading.Thread(target=socket_client)
        t2 = threading.Thread(target=mouse_service)
        t1.start()
        t2.start()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except:
        loop = False