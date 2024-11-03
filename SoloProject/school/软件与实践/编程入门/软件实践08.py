import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
from sklearn.metrics import accuracy_score, classification_report

data = pd.read_csv("voice.csv")
data.head()

# 数据预处理
label = data['label']
del data['label']
# 画图
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文
plt.rcParams['axes.unicode_minus'] = False  # 负号
plt.plot(data, label, 'o')
plt.title('数据分布')
plt.show()

# 数据集
train_data, test_data = train_test_split(data, random_state=1, train_size=0.7, test_size=0.3)
train_label, test_label = train_test_split(label, random_state=1, train_size=0.7, test_size=0.3)
print("the shape of train_data: ", train_data.shape)
print("the shape of test_data: ", test_data.shape)

# 建模
lr = LogisticRegression(max_iter=1000)
lr.fit(train_data, train_label)

pre = lr.predict(test_data)
print("模型精度： ", accuracy_score(test_label, pre))
print("混淆矩阵: \n", confusion_matrix(test_label, pre))
print(classification_report(test_label, pre))
print("查看系数： ", lr.coef_)
