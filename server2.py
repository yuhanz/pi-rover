from flask import Flask, render_template
from flask import stream_with_context, request, Response
import time
import json

app = Flask(__name__)

@app.route('/mpu6050.html')
def jsMpegEndpoint():
    return render_template('mpu6050.html')

@app.route('/stream')
def streamed_response():
    def generate():
        yield "retry: 10000\n"
        while True:
            data = {'acceleration': { 'x' : 1, 'y' : 2, 'z' : 3}, 'gyro': { 'x' : 1, 'y' : 2, 'z' : 3}}
            yield "data: " + json.dumps(data) + "\n\n"
            print("hi")
            time.sleep(2)
    return Response(stream_with_context(generate()), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
