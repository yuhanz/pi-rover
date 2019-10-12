from flask import Flask, render_template
from rover_control import *

import subprocess

app = Flask(__name__)

motorMoveFunctionMap = {
    'stop' : stop,
    'forward': moveForward,
    'backward': moveBackward,
    'left': turnLeft,
    'right': turnRight
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/motor/<move>')
def motorMoveEndpoint():
    move = request.view_args['move']
    func = motorMoveFunctionMap.get(move, None)
    if func:
        func()
        return '{"status": "OK"}'
    else:
        return '{"status": "not found"}'

@app.route('/camera/start')
def cameraStartEndpoint():
    subprocess.call('start-camera.sh')

@app.route('/camera/stop')
def cameraStopEndpoint():
    subprocess.call('kill-camera.sh')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
