# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
from sklearn.preprocessing import QuantileTransformer, LabelEncoder

dataset = pd.read_csv("irrigation_data.csv")

dataset.shape
dataset.head()
X = dataset.drop('label', axis=1)
y = dataset['label']

# encode string status to 0, 1, 2...
le = LabelEncoder()
le.fit(X['weather'])
X['weather'] = le.transform(X['weather'])

# Split X, y to X_train, X_test but not use X_test :))
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

# #normalize data
# quantile_transformer = QuantileTransformer()
# X_train = quantile_transformer.fit_transform(X_train)
# X_test = quantile_transformer.transform(X_test)

classifier = DecisionTreeClassifier()
classifier.fit(X_train, y_train)
classifier2 = classifier.fit(X_train, y_train)

#Testing accuracy of classifier
y_pred = classifier.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Accuracy of classifier: " + str(acc))

# y_pred = classifier.predict(quantile_transformer.transform([[36,40,le.transform(["Clouds"])[0],1.1]]))
y_pred = classifier.predict([[36,40,le.transform(["Clouds"])[0],1.1]])
print(y_pred)

joblib.dump(classifier, 'irrigation.pkl')