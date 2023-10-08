from flask import Flask

app = Flask(__name__)

@app.route('/calibrate')
def calibrate():
    # Your code to receive the signal on your laptop goes here
    return 'Calibration signal received'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
