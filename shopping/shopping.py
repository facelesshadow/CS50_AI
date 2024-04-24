import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

months = {
    "Jan": 0,
    "Feb": 1,
    "Mar": 2,
    "Apr":3,
    "May":4,
    "June":5,
    "Jul":6,
    "Aug":7,
    "Sep":8,
    "Oct":9,
    "Nov":10,
    "Dec":11
}

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

    evidence = []
    label = []
    integers = [0, 2, 4, 10, 11, 12, 13, 14, 15, 16]
    floats = [1, 3, 5, 6, 7, 8, 9]

    with open("shopping.csv") as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            month_name = row[10]
            row[10] = months[month_name]
            

            row[15] = (1 if row[15] == "Returning_Visitor" else 0)
            
            weekend = (1 if row[16] == "TRUE" else 0)
            row[16] = weekend

            purchase = (0 if row[len(row)-1] == "FALSE" else 1)


            for i in integers:
                row[i] = int(row[i])

            for j in floats:
                row[j] = float(row[j])
            
            row.remove(row[17])

            evidence.append(row)
            label.append(purchase) 

    return (evidence, label)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    
    """
    holdout = int(0.50* len(evidence))
    testing_evidence = evidence[:holdout]
    testing_labels = labels[:holdout]
    training_evidence = evidence[holdout:]
    training_labels = labels[holdout:]
    """

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

    correct_true = 0
    total_true = 0
    correct_false = 0
    total_false = 0
    total = 0
    for actual, predicted in zip(labels, predictions):
        total += 1
        if actual == 1:
            total_true += 1
            if actual == predicted:
                correct_true += 1
        elif actual == 0:
            total_false += 1
            if predicted == 0:
                correct_false += 1

    sensitivity = float(correct_true/total_true)
    specificity = float(correct_false/total_false)
    
    return (sensitivity, specificity)

if __name__ == "__main__":
    main()
