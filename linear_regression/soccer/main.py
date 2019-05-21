import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

stats = pd.read_table("../data/regression.csv")
# stats.info()

positional_rating = stats.iloc[:, [0, 1, 2, 3]]
point = stats.iloc[:, 4] / 38   # 球队场均得分
print(positional_rating)
positional_rating_add = sm.add_constant(positional_rating)
print(positional_rating_add)

est_multi = sm.OLS(point, positional_rating_add).fit()
print(est_multi.summary())

fig = plt.figure()
plt.scatter(range(len(point)), est_multi.model.endog, c="b", s=5)
plt.scatter(range(len(point)), est_multi.fittedvalues, c="r", s=5)
plt.title("Multivariate Linear Regression")

plt.show()
