import pandas as pd

df = pd.read_csv("heart_disease_male.csv")

df.sample(5)
df.info()

df['exercice_angina'] = df['exercice_angina'].map(dict(yes=1, no=0))
df['disease'] = df['disease'].map(dict(positive=1, negative=0))

from sklearn.preprocessing import LabelEncoder

df['rest_electro'] = df['rest_electro'].astype('str')
df['chest_pain_type'] = df['chest_pain_type'].astype('str')
df['blood_sugar'] = df['blood_sugar'].astype('bool')

df[['chest_pain_type', 'rest_electro','blood_sugar']] = df[['chest_pain_type', 'rest_electro','blood_sugar']].apply(LabelEncoder().fit_transform)
X=df.iloc[:, 0:13]
X.head()
print('X')
print(X)
df.to_csv('file2.csv')
y=df.iloc[:,-1]
y.head()

patient = [[42,2,160,False,2,136,0,0]]

f = pd.DataFrame (patient, columns = ['age', 'chest_pain_type', 'rest_blood_pressure', 'blood_sugar', 'rest_electro', 'max_heart_rate','exercice_angina','disease'])
print(f)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)
print(X)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
import pandas as pd
print('sad')
print(X_train)

from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
classifier = GaussianNB()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
y_pred1 = classifier.predict(f)

print("y_pred1")
print(y_pred1)
print('Accuracy Score:')
print(metrics.accuracy_score(y_test,y_pred))


from sklearn.metrics import  f1_score
f1_score = f1_score(y_test, y_pred)
print("F1 Score:")
print(f1_score)