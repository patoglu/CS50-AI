import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def convert_visitor_type(visitor):
    return 1 if visitor == "Returning_Visitor" else 0

def convert_boolean(value):
    return 1 if value == "TRUE" else 0

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    month_mapping = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
    "May": 4, "June": 5, "Jul": 6, "Aug": 7,
    "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }


    evidence = []
    labels = []

    with open(filename, newline='') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            evidence.append([
                int(row[0]),
                float(row[1]),
                int(row[2]),
                float(row[3]),
                int(row[4]),
                float(row[5]),
                float(row[6]),
                float(row[7]),
                float(row[8]),
                float(row[9]),
                month_mapping[row[10]],
                int(row[11]),
                int(row[12]),
                int(row[13]),
                int(row[14]),
                convert_visitor_type(row[15]),
                convert_boolean(row[16])
            ])

            labels.append(convert_boolean(row[17]))

    return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    """
    Labels -> The actual ground truth labels in the test data.
    Predictions -> The model's predictions based on the test data.

    Now, I will extract the records from labels where the value is 1. I'll call this set Y.
    Similarly, I will extract the records from predictions where the value is 1, and call this set X.

    However, I need to be careful with X. I should only consider the predictions (1 or 0)
    for the records where the actual label is 1. In other words, X should be filtered based
    on the subset of predictions that correspond to the positive (label = 1) examples.
    """

    tp = 0
    tn = 0
    total_positives = 0
    total_negatives = 0

    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            total_positives += 1
            if predicted == 1:
                tp += 1
        else:
            total_negatives += 1
            if predicted == 0:
                tn += 1


    sensitivity = tp / total_positives if total_positives else 0
    specificity = tn / total_negatives if total_negatives else 0

    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
