# 加载数据
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn import linear_model
a = np.random.rand(1000)
b = np.random.rand(1000)
c = np.random.rand(1000)

noise = np.random.randn(1000, 3)*0.05
print(noise)

input = np.array([a, b, c]).T + noise
target = 5 * a + 10 * b + 15 * c


# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    input, target, test_size=0.4, random_state=0)

# 训练模型
clf = linear_model.LinearRegression()
clf.fit(X_train, y_train)

# 测试模型
accuracy = clf.score(X_test, y_test)
print(accuracy)
print(clf.coef_)

forecast_set = clf.predict(np.array([[1, 2, 3], [4, 5, 6]]))
print(forecast_set)
