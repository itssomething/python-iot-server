from sklearn.externals import joblib
# from sklearn.preprocessing import QuantileTransformer, LabelEncoder
import requests
import json
# quantile_transformer = QuantileTransformer()
# le = LabelEncoder()

def sc(x):
    return {
        'Clear': 1,
        'Clouds': 2,
        'Drizzle': 3,
        'Mist': 4,
        'Thunderstorm': 5
    }[x]


model = joblib.load('irrigation.pkl')
# test = quantile_transformer.transform([[36,80,1,1.1]])
# pred = model.predict([[25,80,4,2.6]])
celsiusTemp = 25
humidityTemp = 60

url = "http://api.openweathermap.org/data/2.5/weather?q=Hanoi,vn&APPID=1364d078d44487625a44d854756268cb"
r = requests.get(url)
data = json.loads(r.text)

weather = data["weather"][0]["main"]
wind = data["wind"]["speed"]
new_weather = sc(weather)

model = joblib.load('irrigation.pkl')
pred = model.predict([[float(celsiusTemp),float(humidityTemp),float(new_weather),float(wind)]])
# return pred[0]
print(pred)