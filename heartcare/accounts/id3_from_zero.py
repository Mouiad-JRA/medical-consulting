import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_recall_fscore_support as score


class GadId3Classifier:
    def fit(self, input, output):
        data = input.copy()
        data[output.name] = output
        self.tree = self.decision_tree(data, data, input.columns, output.name)

    def predict(self, input):
        # convert input data into a dictionary of samples
        samples = input.to_dict(orient='records')
        predictions = []

        # make a prediction for every sample
        for sample in samples:
            predictions.append(self.make_prediction(sample, self.tree, 1.0))

        return predictions

    def entropy(self, attribute_column):
        # find unique values and their frequency counts for the given attribute
        values, counts = np.unique(attribute_column, return_counts=True)

        # calculate entropy for each unique value
        entropy_list = []

        for i in range(len(values)):
            probability = counts[i] / np.sum(counts)
            entropy_list.append(-probability * np.log2(probability))

        # calculate sum of individual entropy values
        total_entropy = np.sum(entropy_list)

        return total_entropy

    def information_gain(self, data, feature_attribute_name, target_attribute_name):
        # find total entropy of given subset
        total_entropy = self.entropy(data[target_attribute_name])

        # find unique values and their frequency counts for the attribute to be split
        values, counts = np.unique(data[feature_attribute_name], return_counts=True)

        # calculate weighted entropy of subset
        weighted_entropy_list = []

        for i in range(len(values)):
            subset_probability = counts[i] / np.sum(counts)
            subset_entropy = self.entropy(
                data.where(data[feature_attribute_name] == values[i]).dropna()[target_attribute_name])
            weighted_entropy_list.append(subset_probability * subset_entropy)

        total_weighted_entropy = np.sum(weighted_entropy_list)

        # calculate information gain
        information_gain = total_entropy - total_weighted_entropy

        return information_gain

    def decision_tree(self, data, original_data, feature_attribute_names, target_attribute_name,
                      parent_node_class=None):
        # base cases:
        # if data is pure, return the majority class of subset
        unique_classes = np.unique(data[target_attribute_name])
        if len(unique_classes) <= 1:
            return unique_classes[0]
        # if subset is empty, ie. no samples, return majority class of original data
        elif len(data) == 0:
            majority_class_index = np.argmax(np.unique(original_data[target_attribute_name], return_counts=True)[1])
            return np.unique(original_data[target_attribute_name])[majority_class_index]
        # if data set contains no features to train with, return parent node class
        elif len(feature_attribute_names) == 0:
            return parent_node_class
        # if none of the above are true, construct a branch:
        else:
            # determine parent node class of current branch
            majority_class_index = np.argmax(np.unique(data[target_attribute_name], return_counts=True)[1])
            parent_node_class = unique_classes[majority_class_index]

            # determine information gain values for each feature
            # choose feature which best splits the data, ie. highest value
            ig_values = [self.information_gain(data, feature, target_attribute_name) for feature in
                         feature_attribute_names]
            best_feature_index = np.argmax(ig_values)
            best_feature = feature_attribute_names[best_feature_index]

            # create tree structure, empty at first
            tree = {best_feature: {}}

            # remove best feature from available features, it will become the parent node
            feature_attribute_names = [i for i in feature_attribute_names if i != best_feature]

            # create nodes under parent node
            parent_attribute_values = np.unique(data[best_feature])
            for value in parent_attribute_values:
                sub_data = data.where(data[best_feature] == value).dropna()

                # call the algorithm recursively
                subtree = self.decision_tree(sub_data, original_data, feature_attribute_names, target_attribute_name,
                                             parent_node_class)

                # add subtree to original tree
                tree[best_feature][value] = subtree

            return tree

    def make_prediction(self, sample, tree, default=1):
        # map sample data to tree
        for attribute in list(sample.keys()):
            # check if feature exists in tree
            if attribute in list(tree.keys()):
                try:
                    result = tree[attribute][sample[attribute]]
                except:
                    return default

                result = tree[attribute][sample[attribute]]

                # if more attributes exist within result, recursively find best result
                if isinstance(result, dict):
                    return self.make_prediction(sample, result)
                else:
                    return result


def id3_hard(dataset, age, chest_pain_type, rest_blood_pressure, blood_sugar, rest_electro, max_heart_rate,
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
    model = GadId3Classifier()
    model.fit(X_train, y_train)

    f = pd.DataFrame(patient, columns=['age', 'chest_pain_type', 'rest_blood_pressure', 'blood_sugar', 'rest_electro',
                                       'max_heart_rate', 'exercice_angina'])

    y_pred = model.predict(f)
    yy_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, yy_pred)
    precision, recall, fscore, support = score(y_test, yy_pred, average='macro')
    print('Precision for id3 from zero : {}'.format(precision))
    print('Recall for id3 from zero  : {}'.format(recall))
    print('F-score for id3 from zero : {}'.format(fscore))
    print('Accuracy for id3 from zero : {}'.format(accuracy))
    return y_pred[0], accuracy, precision, recall, fscore
