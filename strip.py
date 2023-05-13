from flask import Flask

app = Flask(__name__)
@app.route('/robot<int:x>/<int:r>')
def robot(x,r):
    return f'Robot {x} {r} deg'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    