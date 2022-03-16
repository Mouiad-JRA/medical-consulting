

def sklearn_algorithm(dataset, age, chest_pain_type, rest_blood_pressure, blood_sugar, rest_electro, max_heart_rate,
                      exercice_angina):
    import pandas as pd

    df = pd.read_csv(dataset)
    df.sample(5)
    df.info()

    df['exercice_angina'] = df['exercice_angina'].map(dict(yes=1, no=0))
    df['disease'] = df['disease'].map(dict(positive=1, negative=0))

    from sklearn.preprocessing import LabelEncoder

    df['rest_electro'] = df['rest_electro'].astype('str')
    df['chest_pain_type'] = df['chest_pain_type'].astype('str')
    df['blood_sugar'] = df['blood_sugar'].astype('bool')

    df[['chest_pain_type', 'rest_electro', 'blood_sugar']] = df[
        ['chest_pain_type', 'rest_electro', 'blood_sugar']].apply(LabelEncoder().fit_transform)
    X = df.iloc[:, 0:7]
    X.head()
    print('X')
    y = df.iloc[:, -1]
    y.head()
    if(chest_pain_type=='asympt'):
        cpt = 0
    elif (chest_pain_type=='atyp_angina'):
        cpt = 1
    elif (chest_pain_type=='non_anginal'):
        cpt = 2

    if (blood_sugar==False):
        bs= 0
    elif (blood_sugar):
        bs =1

    if (rest_electro=='normal'):
        re = 2
    elif (rest_electro=='left_vent_hyper'):
        re = 1
    elif (rest_electro=='st_t_wave_abnormality'):
        re = 3

    if (exercice_angina):
        ea= 1
    elif (exercice_angina==False):
        ea= 0

    patient = [[age, cpt, rest_blood_pressure, bs, re, max_heart_rate, ea]]

    f = pd.DataFrame(patient, columns=['age', 'chest_pain_type', 'rest_blood_pressure', 'blood_sugar', 'rest_electro',
                                       'max_heart_rate', 'exercice_angina'])

    print(f)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    from sklearn.naive_bayes import GaussianNB
    classifier = GaussianNB()
    classifier.fit(X_train, y_train)
    p = scaler.transform(patient)
    y_pred = classifier.predict(p)


    return y_pred[0]

