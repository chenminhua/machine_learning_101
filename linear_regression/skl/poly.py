from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

sample_num = 1000
x = (np.random.rand(sample_num) - 0.5) * 20
y = np.sqrt(100 - x * x) + np.random.randn(sample_num) * 0.2

fig = plt.figure(figsize=(10, 10))
plt.scatter(x, y)
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4, random_state=0)

poly = PolynomialFeatures(degree=2)
X_train = poly.fit_transform(X_train.reshape(-1, 1))
# y_train = ploy.fit_transform(y_train)
clf = linear_model.LinearRegression()
clf.fit(X_train, y_train)

accuracy = clf.score(poly.fit_transform(X_test.reshape(-1, 1)), y_test)
print(accuracy)
print(clf.coef_)
