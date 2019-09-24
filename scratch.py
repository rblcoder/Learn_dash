import pandas as pd
from sklearn import datasets
iris = datasets.load_iris()
#print(iris.data)
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
print(df.describe())
print(iris.filename)
print(df.describe().index[0])
