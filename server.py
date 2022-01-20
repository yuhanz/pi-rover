from flask import Flask, render_template
from flask import stream_with_context, request, Response
from rover_control import *
import time
import subprocess

from mpu6050 import mpu6050
import json

sensor = mpu6050(0x68)

app = Flask(__name__)

motorMoveFunctionMap = {
    'stop' : stop,
    'forward': moveForward,
    'backward': moveBackward,
    'left': turnLeft,
    'right': turnRight
}


@app.route('/')
def indexEndpoint():
    return render_template('index.html')

@app.route('/jsmpeg.min.js')
def jsMpegEndpoint():
    return render_template('jsmpeg.min.js')

@app.route('/mpu6050.html')
def mpu6050():
    return render_template('mpu6050.html')


@app.route('/motor/<move>')
def motorMoveEndpoint(move):
    func = motorMoveFunctionMap.get(move, None)
    if func:
        func()
        return '{"status": "OK"}'
    else:
        return '{"status": "not found"}'

@app.route('/camera/start')
def cameraStartEndpoint():
    subprocess.call('./start-camera.sh')
    return '{"status": "OK"}'

@app.route('/camera/stop')
def cameraStopEndpoint():
    subprocess.call('./kill-camera.sh')
    return '{"status": "OK"}'

@app.route('/stream')
def streamed_response():
    def generate():
        yield "retry: 5000\n"
        while True:
            accel_data = sensor.get_accel_data()
            gyro_data = sensor.get_gyro_data()
            data = {'acceleration': accel_data, 'gyro': gyro_data}
            yield "data: "+ json.dumps(data) +"\n\n"
            time.sleep(1)
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
