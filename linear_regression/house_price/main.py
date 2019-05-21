#!/usr/bin/env python
# coding=utf-8
import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

train = pd.read_csv('../../data/house_price/train.csv')
# print(train.head())
# 一共81列，1460行
print(train.info())


# # 下面我们分析下目标数据salePrice是否符合正态分布
# plt.subplots(figsize=(12, 9))
# sns.distplot(train['SalePrice'], fit=stats.norm)

# # Get the fitted parameters used by the function

# (mu, sigma) = stats.norm.fit(train['SalePrice'])

# # plot with the distribution

# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(
#     mu, sigma)], loc='best')
# plt.ylabel('Frequency')
# # Probablity plot
# fig = plt.figure()
# stats.probplot(train['SalePrice'], plot=plt)
# plt.show()
# ppplot : Probability-Probability plot Compares the sample and theoretical probabilities (percentiles).
# qqplot : Quantile-Quantile plot Compares the sample and theoretical quantiles
# probplot : Probability plot Same as a Q-Q plot, however probabilities are shown in the scale of the theoretical distribution (x-axis) and the y-axis contains unscaled quantiles of the sample data.


# 把salePrice转成正态分布
train['SalePrice'] = np.log1p(train['SalePrice'])

# Check again for more normal distribution

# plt.subplots(figsize=(12, 9))
# sns.distplot(train['SalePrice'], fit=stats.norm)

# # Get the fitted parameters used by the function

# (mu, sigma) = stats.norm.fit(train['SalePrice'])

# # plot with the distribution

# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(
#     mu, sigma)], loc='best')
# plt.ylabel('Frequency')

# Probablity plot

# fig = plt.figure()
# stats.probplot(train['SalePrice'], plot=plt)
# plt.show()


# 处理空值列
print(train.columns[train.isnull().any()])
print(sum(train['FireplaceQu'].isnull()))

# 先用heatmap查看空值情况
plt.figure(figsize=(12, 6))
sns.heatmap(train.isnull())
plt.show()

Isnull = train.isnull().sum()/len(train)*100
Isnull = Isnull[Isnull > 0]
Isnull.sort_values(inplace=True, ascending=False)
print(Isnull)
