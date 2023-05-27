from flask import Flask
import threading
import logging
import time
import sys
import os

app = Flask(__name__)
FLASK_PORT = 5000

@app.route('/')
def hello_world():
    return 'Base Station'

@app.route('/robot<int:x>/<string:r>')
def robot(x,r):
    robot_id = x
    robot_sensor = r
    if robot_id == 1:
        #kirim data sensor ke robot 1 pakai socket, mangats
        pass
    if robot_id == 2:
        #kirim data sensor ke robot 2 pakai socket, mangats
        pass
    return f'{robot_id}{robot_sensor}'

def run_flask():
    try: app.run(debug=True, use_reloader=False, host='0.0.0.0', port=FLASK_PORT)
    except RuntimeError as msg:
        if str(msg) == "Server going down":
            pass

def run_main_program(run_event):
    while run_event.is_set():
        # print("intinya run_event sama logika while di atas harus ada di setiap thread (kecuali yang flask)")
        time.sleep(2)

if __name__ == '__main__':
    own_pid = os.getpid()
    try:
        run_event = threading.Event()
        run_event.set()

        logging.info(f'start flask thread')
        t1 = threading.Thread(target=run_flask).start()

        logging.info(f'start main thread')
        t2 = threading.Thread(target=run_main_program, args=(run_event,)).start()
        
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
