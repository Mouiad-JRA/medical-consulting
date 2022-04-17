from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_fscore_support as score


def id3(dataset, age, chest_pain_type, rest_blood_pressure, blood_sugar, rest_electro, max_heart_rate,
        exercice_angina):
    df = pd.read_csv(dataset)
    df.sample(5)
    print(df.head())

    df['exercice_angina'] = df['exercice_angina'].map(dict(yes=1, no=0))
    df['disease'] = df['disease'].map(dict(positive=1, negative=0))

    df['rest_electro'] = df['rest_electro'].astype('str')
    df['chest_pain_type'] = df['chest_pain_type'].astype('str')
    df['blood_sugar'] = df['blood_sugar'].astype('bool')

    df[['chest_pain_type', 'rest_electro', 'blood_sugar']] = df[
        ['chest_pain_type', 'rest_electro', 'blood_sugar']].apply(LabelEncoder().fit_transform)

    # organize data into input and output
    X = df.iloc[:, 0:7]
    y = df.iloc[:, -1]

    if chest_pain_type == 'asympt':
        cpt = 0
    elif chest_pain_type == 'atyp_angina':
        cpt = 1
    elif chest_pain_type == 'non_anginal':
        cpt = 2

    if not blood_sugar:
        bs = 0
    elif blood_sugar:
        bs = 1

    if rest_electro == 'normal':
        re = 2
    elif rest_electro == 'left_vent_hyper':
        re = 1
    elif rest_electro == 'st_t_wave_abnormality':
        re = 3

    if exercice_angina:
        ea = 1
    elif not exercice_angina:
        ea = 0

    patient = [[age, cpt, rest_blood_pressure, bs, re, max_heart_rate, ea]]

    f = pd.DataFrame(patient, columns=['age', 'chest_pain_type', 'rest_blood_pressure', 'blood_sugar', 'rest_electro',
                                       'max_heart_rate', 'exercice_angina'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

    # initialize and fit model
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(X_train, y_train)

    f = pd.DataFrame(patient, columns=['age', 'chest_pain_type', 'rest_blood_pressure', 'blood_sugar', 'rest_electro',
                                       'max_heart_rate', 'exercice_angina'])

    y_pred = model.predict(f)
    yy_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, yy_pred)
    precision, recall, fscore, support = score(y_test, yy_pred, average='macro')
    print('Precision for id3 : {}'.format(precision))
    print('Recall for id3   : {}'.format(recall))
    print('F-score for id3  : {}'.format(fscore))
    print('Accuracy for id3  : {}'.format(accuracy))
    return y_pred[0], accuracy, precision, recall, fscore
