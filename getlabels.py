"""
Getting labels for the data, adding the labels as attributes to the datapoints as well as returning the labels themselves.

Input to instrumentsToLabels should look like this:
{
    train: [datapoints],
    test:  [datapoints]
}

Output of instrumentsToLabels should look like this:
{
    train: [label_ints],
    test: [label_ints]
}

Once we create the initial encoding of labels for the training dataset, we want to remove any test datapoints that have a label that isn't in the training dataset.
"""
from sklearn.preprocessing.label import LabelEncoder

def instrumentsToLabels(splitData):
    # input should look like {train: [datapoints], test: [datapoints]}
    le = LabelEncoder()
    labels = { "le": le } # we want to keep track of le because its the only way to decode what each label means

    train_instruments = [dp["instrument"] for dp in splitData["train"]]
    labels["train"] = le.fit_transform(train_instruments)

    removeUnseenClasses(splitData, le, "instrument")

    test_instruments = [dp["instrument"] for dp in splitData["test"]]
    labels["test"] = le.transform(test_instruments)

    return labels

def categoryToLabels(splitData):
    # same as above but working with instrument_category instead of instrument
    le = LabelEncoder()
    labels = { "le": le }

    train_categories = [dp["instrument_category"] for dp in splitData["train"]]
    labels["train"] = le.fit_transform(train_categories)

    removeUnseenClasses(splitData, le, "instrument_category")

    test_categories = [dp["instrument_category"] for dp in splitData["test"]]
    labels["test"] = le.transform(test_categories)

    return labels

def removeUnseenClasses(splitData, le, key):
    # remove labels that aren't in the training data from the test data
    splitData["test"] = [
        dp for dp in splitData["test"]
        if dp[key] in le.classes_
    ]
