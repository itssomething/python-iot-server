import pandas
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
# import matplotlib.pyplot as plt

df=pandas.read_csv('./water_amount_data.csv')

X=df[list(df.columns)[:-1]]
Y=df[list(df.columns)[-1]]

xtrain,xtest,ytrain,ytest=train_test_split(X,Y,random_state=0)

linear_reg = LinearRegression()

linear_reg.fit(xtrain, ytrain)
# y_pred = linear_reg.predict(xtest)
# acc = accuracy_score(ytest, y_pred)
# print("Accuracy of classifier: " + str(acc))

joblib.dump(linear_reg, 'water_amount.pkl')
# plt.scatter(df['temp'], df['humidity'], color='red')