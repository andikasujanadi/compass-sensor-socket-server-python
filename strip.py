from flask import Flask
r1_rot = 0
r2_rot = 0

app = Flask(__name__)
@app.route('/robot<int:x>/<int:r>')
def robot(x,r):
    if x == 1:
        global r1_rot
        r1_rot = r
    elif x == 2:
        global r2_rot
        r2_rot = r
    return f'Robot {x} {r} deg'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)