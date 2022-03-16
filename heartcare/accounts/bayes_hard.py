# Importing library
import math
import random
import csv


def encode_class(mydata):
    classes = []
    for i in range(len(mydata)):
        if mydata[i][-1] not in classes:
            classes.append(mydata[i][-1])
    for i in range(len(classes)):
        for j in range(len(mydata)):
            if mydata[j][-1] == classes[i]:
                mydata[j][-1] = i
    return mydata


def splitting(mydata, ratio):
    train_num = int(len(mydata) * ratio)
    train = []
    test = list(mydata)
    while len(train) < train_num:
        index = random.randrange(len(test))
        train.append(test.pop(index))
    return train, test


def groupUnderClass(mydata):
    dict = {}
    for i in range(len(mydata)):
        if (mydata[i][-1] not in dict):
            dict[mydata[i][-1]] = []
        dict[mydata[i][-1]].append(mydata[i])
    return dict


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def std_dev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def MeanAndStdDev(mydata):
    info = [(mean(attribute), std_dev(attribute)) for attribute in zip(*mydata)]
    del info[-1]
    return info


def MeanAndStdDevForClass(mydata):
    info = {}
    dict = groupUnderClass(mydata)
    for classValue, instances in dict.items():
        info[classValue] = MeanAndStdDev(instances)
    return info


def calculateGaussianProbability(x, mean, stdev):
    expo = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * expo


def calculateClassProbabilities(info, test):
    probabilities = {}
    for classValue, classSummaries in info.items():
        probabilities[classValue] = 1
        for i in range(len(classSummaries)):
            mean, std_dev = classSummaries[i]
            x = test[i]
            probabilities[classValue] *= calculateGaussianProbability(x, mean, std_dev)
    return probabilities


def predict(info, test):
    probabilities = calculateClassProbabilities(info, test)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.items():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel


def getPredictions(info, test):
    predictions = []
    for i in range(len(test)):
        result = predict(info, test[i])
        predictions.append(result)
    return predictions


def accuracy_rate(test, predictions):
    correct = 0
    for i in range(len(test)):
        if test[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(test))) * 100.0


def sklearn_algorithm_from_scratch(dataset, age, chest_pain_type, rest_blood_pressure, blood_sugar, rest_electro,
                                   max_heart_rate,
                                   exercice_angina):
    mydata = csv.reader(open(dataset, "rt"))
    mydata = list(mydata)
    mydata = encode_class(mydata)
    for i in range(len(mydata)):
        mydata[i] = [float(x) for x in mydata[i]]

    ratio = 0.7
    train_data, test_data = splitting(mydata, ratio)
    print('Total number of examples are: ', len(mydata))
    print('Out of these, training examples are: ', len(train_data))
    print("Test examples are: ", len(test_data))

    info = MeanAndStdDevForClass(train_data)
    if (chest_pain_type == 'asympt'):
        cpt = 0
    elif (chest_pain_type == 'atyp_angina'):
        cpt = 1
    elif (chest_pain_type == 'non_anginal'):
        cpt = 2

    if (blood_sugar == False):
        bs = 0
    elif (blood_sugar):
        bs = 1

    if (rest_electro == 'normal'):
        re = 2
    elif (rest_electro == 'left_vent_hyper'):
        re = 1
    elif (rest_electro == 'st_t_wave_abnormality'):
        re = 3

    if (exercice_angina):
        ea = 1
    elif (exercice_angina == False):
        ea = 0

    patient = [[age, cpt, rest_blood_pressure, bs, re, max_heart_rate, ea]]
    predictions_for_one_sample = getPredictions(info, patient)
    print("The predictions is: ", predictions_for_one_sample)
    return predictions_for_one_sample[0]
