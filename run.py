from flask import Flask
from flask import request
from flask import jsonify
from sklearn.externals import joblib
import json
import requests
from flask_apscheduler import APScheduler
import math
import numpy
import multiprocessing
from multiprocessing.dummy import Pool
from multiprocessing import Process

import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

my_awesome_app = Flask(__name__)

# def print_date_time():
#     # print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# 	url = "http://192.168.43.150?ab=0"
# 	r = requests.get(url)
#     print(str(r))
#     return "123"
# 	return str(r)
lat = ""
lon = ""

def sc(x):
    return {
        'Clear': 1,
        'Clouds': 2,
        'Drizzle': 3,
        'Mist': 4,
        'Thunderstorm': 5,
        'Rain': 5
    }[x]

esp_url = "http://192.168.43.150"

def send_request_to_arduino(url):
	requests.get(url)


def schedule_check():
	sensor_url = esp_url + "?ab=3"
	sensor_text = requests.get(sensor_url)
	sensor_data = json.loads(sensor_text.text)
	celsiusTemp = sensor_data["celsiusTemp"]
	humidityTemp = sensor_data["humidityTemp"]


	url = "http://api.openweathermap.org/data/2.5/weather?q=Hanoi,vn&APPID=1364d078d44487625a44d854756268cb"
	r = requests.get(url)
	data = json.loads(r.text)

	weather = data["weather"][0]["main"]
	wind = data["wind"]["speed"]
	new_weather = sc(weather)

	model = joblib.load('irrigation.pkl')
	pred = model.predict([[float(celsiusTemp),float(humidityTemp),float(new_weather),float(wind)]])

	cond = pred.astype(int)[0].astype(int).item()
	int_cond =  int(str(cond))
	print(int_cond)
	if int_cond == 1:
		model_water_amount = joblib.load('water_amount.pkl')
		pred2 = model_water_amount.predict([[float(celsiusTemp),float(humidityTemp),float(wind)]])
		amount = math.ceil(pred2.astype(float)[0].astype(float).item())
		print(amount)

		water_url = esp_url + "?ab=1&cd=" + str(amount*1000)
		requests.get(water_url)
		print(water_url)
		return "water"
	else:
		return "not watering"

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=schedule_check, trigger="interval", seconds=180)
# scheduler.start()

# atexit.register(lambda: scheduler.shutdown())

@my_awesome_app.route('/')
def hello_world():
    return 'Hello World!'

@my_awesome_app.route('/api', methods=['GET'])
def get_sensor_info():
	sensor_url = esp_url + "?ab=3"
	sensor_text = requests.get(sensor_url)
	sensor_data = json.loads(sensor_text.text)
	celsiusTemp = sensor_data["celsiusTemp"]
	humidityTemp = sensor_data["humidityTemp"]

	# set up lat and long
	global lat
	global lon
	lat = request.args["lat"]
	lon = request.args["lon"]
	print(lat)

	return jsonify(celsiusTemp=celsiusTemp,
                   humidityTemp=humidityTemp)

@my_awesome_app.route('/test', methods=['GET'])
def test_weather_api():
	# url = "http://api.openweathermap.org/data/2.5/weather?q=Hanoi,vn&APPID=1364d078d44487625a44d854756268cb"
	# print(lat)
	global lat
	global lon
	url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&APPID=1364d078d44487625a44d854756268cb"

	print(url)
	r = requests.get(url)
	data = json.loads(r.text)

	weather = data["weather"][0]["main"]

	return weather

@my_awesome_app.route('/api/water-time', methods=['POST'])
def water_post_api():
	req_data = request.get_json()
	time_var = int(req_data["time"])
	print(time_var == -1)
	if time_var != -1 and time_var != 0: # tuoi theo thoi gian
		time_var = int(req_data["time"]) * 1000
		url = esp_url + "?ab=1&cd=" + str(time_var)
		requests.get(url)
		return "sent normal"
	elif time_var == 0: # dung
		url = esp_url + "?ab=0"
		requests.get(url)
		return "sent 0"
	elif time_var == -1: # tuoi mai mai
		url = esp_url + "?ab=2"
		requests.get(url)
		print("sent request")
		return "sent -1"


@my_awesome_app.route('/api/water-ai', methods=['GET'])
def api_with_ai():
	sensor_url = esp_url + "?ab=3"
	sensor_text = requests.get(sensor_url)
	sensor_data = json.loads(sensor_text.text)
	celsiusTemp = sensor_data["celsiusTemp"]
	humidityTemp = sensor_data["humidityTemp"]

	# url = "http://api.openweathermap.org/data/2.5/weather?q=Hanoi,vn&APPID=1364d078d44487625a44d854756268cb"

	global lat
	global lon
	url = "http://api.openweathermap.org/data/2.5/weather?lat=" + str(lat) + "&lon=" + str(lon) + "&APPID=1364d078d44487625a44d854756268cb"

	r = requests.get(url)
	data = json.loads(r.text)

	weather = data["weather"][0]["main"]
	wind = data["wind"]["speed"]
	new_weather = sc(weather)

	model = joblib.load('irrigation.pkl')
	pred = model.predict([[float(celsiusTemp),float(humidityTemp),float(new_weather),float(wind)]])

	cond = pred.astype(int)[0].astype(int).item()
	int_cond =  int(str(cond))
	print(int_cond)
	if int_cond == 1:
		model_water_amount = joblib.load('water_amount.pkl')
		pred2 = model_water_amount.predict([[float(celsiusTemp),float(humidityTemp),float(wind)]])
		amount = math.ceil(pred2.astype(float)[0].astype(float).item())
		print(amount)

		water_url = esp_url + "?ab=1&cd=" + str(amount*1000)
		p = Process(target=send_request_to_arduino, args=(water_url,))
		p.start()
		# requests.get(water_url)

		print(water_url)
		return jsonify(celsiusTemp=int_cond, humidityTemp=amount)
		p.join()
	else:
		amount = 0
		return jsonify(celsiusTemp=int_cond, humidityTemp=amount)

@my_awesome_app.route('/api/water-cord', methods=['POST'])
def water_with_cord():
	req_data = request.get_json()
	lat = int(req_data["lat"])
	lon = int(req_data["lon"])



	return "123"
if __name__ == '__main__':
    my_awesome_app.run('0.0.0.0')
