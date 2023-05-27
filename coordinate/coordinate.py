from flask import Flask
import threading
import requests
import logging
import time
import sys
import os

app = Flask(__name__)
ROBOT_ID = 1
LOCAL_FLASK_PORT = 6000
BASESTATION_FLASK_ADDR = 'http://127.0.0.1:5000'

angle = 0
robot_id = 1
reset_pos = False

@app.route('/')
def hello_world():
    return 'Sensor Server'

@app.route('/robot<int:x>/<int:r>')
def robot(x,r):
    global robot_id
    global angle
    robot_id = x
    angle = r
    return f'angle'

@app.route('/resetpos<int:x>')
def reset_position(x):
    if x == ROBOT_ID:
        global reset_pos
        reset_pos = True
    return f'reset'
        
def mouse_service(run_event):
    import pyautogui
    import math
    print('mouse service is on!')
    global robot_id
    global angle
    global loop
    global for_socket
    global reset_pos

    init_x=960
    init_y=540
    boundary = 400
    x0, y0 = init_x, init_y
    x, y = 0, 0
    x_fix, y_fix = 0, 0
    point_per_m = 1735
    pyautogui.moveTo(init_x, init_y)
    for_basestation_old = ''

    while run_event.is_set():

        if reset_pos:
            reset_pos = False
            x0, y0 = init_x, init_y
            x, y = 0, 0
            x_fix, y_fix = 0, 0
            pyautogui.moveTo(init_x, init_y)

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

        if robot_id == ROBOT_ID:
            for_basestation = f'R{robot_id}{to3d(angle)}{"-" if x_fix<0 else "+"}{to3d(x_fix)}{"-" if y_fix<0 else "+"}{to3d(y_fix)}'
            print(for_basestation, end='')
            print('\b' * len(for_basestation), end='', flush=True)
            if for_basestation != for_basestation_old:
                try:
                    requests.get(f'{BASESTATION_FLASK_ADDR}/robot1/{for_basestation}', verify=False, timeout=0.3)
                except: pass
            for_basestation_old = for_basestation
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

def run_flask():
    try: app.run(debug=True, use_reloader=False, host='0.0.0.0', port=LOCAL_FLASK_PORT)
    except RuntimeError as msg:
        if str(msg) == "Server going down":
            pass

if __name__ == '__main__':
    own_pid = os.getpid()
    try:
        run_event = threading.Event()
        run_event.set()

        logging.info(f'start flask thread')
        t1 = threading.Thread(target=run_flask).start()

        logging.info(f'start main thread')
        t2 = threading.Thread(target=mouse_service, args=(run_event,)).start()

        try:
            while True: time.sleep(.1)

        except KeyboardInterrupt:
            run_event.clear()
            os.kill(own_pid, 9)
            t1.join()
            t2.join()

    except Exception as e:
        logging.error("Unexpected error:" + str(e))
        sys.exit()