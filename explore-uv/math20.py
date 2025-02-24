import numpy as np
import pandas as pd

data = pd.read_csv('C:/Users/aleja/Downloads/iris.csv')

X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

y_encoded = pd.Categorical(y).codes

np.random.seed(42)

train_X, test_X = [], []
train_y, test_y = [], []

for label in np.unique(y_encoded):
    indices = np.where(y_encoded == label)[0]
    np.random.shuffle(indices)
    train_indices = indices[:40]
    test_indices = indices[40:]

    train_X.append(X[train_indices])
    test_X.append(X[test_indices])

    train_y.append(y_encoded[train_indices])
    test_y.append(y_encoded[test_indices])

train_X = np.vstack(train_X)
train_y = np.hstack(train_y)
test_X = np.vstack(test_X)
test_y = np.hstack(test_y)

train_X = np.c_[np.ones(train_X.shape[0]), train_X]
test_X = np.c_[np.ones(test_X.shape[0]), test_X]

XtX_inv = np.linalg.inv(train_X.T @ train_X)
XtY = train_X.T @ train_y
beta = XtX_inv @ XtY

predictions = test_X @ beta
predicted_labels = np.round(predictions).astype(int)
incorrect_predictions = np.sum(predicted_labels != test_y)

print(f"Number of incorrect predictions: {incorrect_predictions}")
print(np.unique(train_y, return_counts=True)) 
print(np.unique(test_y, return_counts=True))
