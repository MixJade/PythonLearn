import pandas as pd
from sklearn import svm

data = [[0.697, 0.460, 1],
        [0.774, 0.376, 1],
        [0.634, 0.264, 1],
        [0.608, 0.318, 1],
        [0.556, 0.215, 1],
        [0.430, 0.237, 1],
        [0.481, 0.149, 1],
        [0.437, 0.211, 1],
        [0.666, 0.091, 0],
        [0.243, 0.267, 0],
        [0.245, 0.057, 0],
        [0.343, 0.099, 0],
        [0.639, 0.161, 0],
        [0.657, 0.198, 0],
        [0.360, 0.370, 0],
        [0.593, 0.042, 0],
        [0.719, 0.103, 0]]
column = ['密度', '含糖', '好瓜']
dataSet = pd.DataFrame(data, columns=column)
X = dataSet[['密度', '含糖']].values
Y = dataSet['好瓜'].values

for fig_num, kernel in enumerate(('linear', 'rbf')):
    svc = svm.SVC(C=1000, kernel=kernel)
    svc.fit(X,Y)
    sv = svc.support_vectors_
    sv_id = svc.support_
    sv_num = svc.n_support_
    print('{}核函数的支持向量为\n{}，\n支持向量的下标为{}，\n支持向量个数为{}'.format(kernel, sv, sv_id, sv_num))
