import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from collections import Counter
import 软件实践06


def pca_reduce(data):
    dim_data = np.shape(data)
    pca = PCA(n_components=dim_data[1] - 1)
    projected = pca.fit_transform(data)
    s = pca.explained_variance_
    c_s = pd.DataFrame({'tb': s,
                        'b_sum': s.cumsum() / s.sum()})
    plt.xlabel("Number of Principal components")
    plt.ylabel("Contribution Rate")
    c_s['b_sum'].plot(style='--ko', figsize=(10, 4))
    plt.axhline(0.85, color='r', linestyle='--', alpha=0.8)
    plt.text(x=dim_data[1] - 3, y=c_s['b_sum'].iloc[6] - 0.08, s='85%', color='r')
    plt.show()
    num = Counter(c_s['b_sum'] >= 0.85)[0]
    pca = PCA(n_components=num)
    reduce_data = pca.fit_transform(X)
    return reduce_data


if __name__ == '__main__':
    """模型测试"""
    X, y = [], []
    filename = "../venv/data1_KNN.xlsx"
    df = pd.read_excel(filename)
    df.head(5)
    y = df['购买意愿']
    df = df.drop(['目标客\n户编号', '购买意愿'], axis=1)
    X = np.array(df)
    y = np.array(y)
    X = pca_reduce(X)

    """训练误差"""
    knc = 张涛实验6.KNeighborsClassifier(10)
    knc.fit(X, y)
    print("训练准确率: ", knc.score(X, y))  # 0.963
    print()

    """测试误差"""
    r1 = int(np.shape(X)[0] * 0.7)
    r2 = np.shape(X)[0] - r1
    X_train, X_test = X[:r1], X[-r2:]
    y_train, y_test = y[:r1], y[-r2:]
    knc = 张涛实验6.KNeighborsClassifier(10)
    knc.fit(X_train, y_train)
    print("测试准确率: ", knc.score(X_test, y_test))
