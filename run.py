from flask import Flask
from flask import request
from flask import jsonify
import json
import requests

my_awesome_app = Flask(__name__)


@my_awesome_app.route('/')
def hello_world():
    return 'Hello World!'

@my_awesome_app.route('/api/diabetes', methods=['POST'])
def diabetes_api():
	req_data = request.get_json()
	print(req_data)
	celsiusTemp = req_data["celsiusTemp"]
	humidityTemp = req_data["humidityTemp"]
	print(celsiusTemp)
	print(" ")
	print(humidityTemp)

	return celsiusTemp

@my_awesome_app.route('/api', methods=['GET'])
def get_sensor_info():
	celsiusTemp = 27.1
	humidityTemp = 69.2
	print(request.args.get('test'))
	#string = '{"celsiusTemp":"' + celsiusTemp + '",' + '"humidityTemp":"' + humidityTemp + '"}'
	return jsonify(celsiusTemp=celsiusTemp,
                   humidityTemp=humidityTemp)

@my_awesome_app.route('/test', methods=['GET'])
def test_weather_api():
	url = "http://api.openweathermap.org/data/2.5/weather?q=Hanoi,vn&APPID=1364d078d44487625a44d854756268cb"
	r = requests.get(url)
	data = json.loads(r.text)

	weather = data["weather"][0]["main"]

	return weather

@my_awesome_app.route('/api/water', methods=['POST'])
def water_post_api():
	req_data = request.get_json()
	time = req_data["time"]

	return jsonify(time=time)


if __name__ == '__main__':
    my_awesome_app.run('0.0.0.0')
