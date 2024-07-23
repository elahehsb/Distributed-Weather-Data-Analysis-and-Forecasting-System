from flask import Flask, render_template, jsonify
import subprocess
from influxdb import InfluxDBClient

app = Flask(__name__)
client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('weather')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/weather')
def weather():
    results = client.query('SELECT * FROM weather')
    points = list(results.get_points())
    return jsonify(points)

@app.route('/api/forecast')
def forecast():
    result = subprocess.run(['spark-submit', 'machine_learning/weather_forecasting_model.py'], capture_output=True, text=True)
    return jsonify({"result": result.stdout})

if __name__ == '__main__':
    app.run(debug=True)
