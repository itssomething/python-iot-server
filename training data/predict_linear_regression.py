from sklearn.externals import joblib

model = joblib.load('water_amount.pkl')
pred = model.predict([[25,60,2.6]])
print(pred)