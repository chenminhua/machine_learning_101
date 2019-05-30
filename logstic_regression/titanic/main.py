from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn import linear_model
data = pd.read_csv('../../data/titanic.csv')   # DataFrame
data.describe()


data = a.ix[:, ['Survived', 'Pclass', 'Sex', 'Age', 'Fare']]
data['Sex'] = data['Sex'].apply(lambda sex:  1 if sex == 'female' else -1)
data = data.fillna(data.mean()['Age':'Fare'])
target = data['Survived']
input = data.drop('Survived', axis=1)


X_train, X_test, y_train, y_test = train_test_split(
    input, target, test_size=0.2, random_state=0)


clf = LogisticRegression(C=1., solver='lbfgs')


clf.fit(X_train, y_train)

clf.score(X_test, y_test)
