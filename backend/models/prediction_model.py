import numpy as np
from sklearn.linear_model import LogisticRegression

# Dummy training data
# [attendance %, marks]
X = np.array([
    [90, 85],
    [80, 75],
    [70, 65],
    [60, 50],
    [50, 40],
    [40, 30]
])

# 1 = Pass, 0 = Fail
y = np.array([1, 1, 1, 1, 0, 0])

# Train model
model = LogisticRegression()
model.fit(X, y)


def predict_result(attendance, marks):

    data = np.array([[attendance, marks]])

    result = model.predict(data)[0]

    if result == 1:
        return "Pass"
    else:
        return "Fail"