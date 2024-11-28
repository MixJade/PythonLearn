from sklearn import svm
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

iris = load_iris()
n_samples, n_feature = iris.data.shape
print("dim: ", (n_samples, n_feature))
print("key: ", iris.keys())

train_data, test_data = train_test_split(iris.data, random_state=1, train_size=0.7, test_size=0.3)
train_label, test_label = train_test_split(iris.target, random_state=1, train_size=0.7, test_size=0.3)

gamma = 10
print("gamma= ", gamma)
classifier = svm.SVC(C=2, kernel='rbf', gamma=gamma, decision_function_shape='ovr')
classifier.fit(train_data, train_label.ravel())

pre_train = classifier.predict(train_data)
pre_test = classifier.predict(test_data)
print("train= ", accuracy_score(train_label, pre_train))
print("test= ", accuracy_score(test_label, pre_test))

print("混淆矩阵\n", confusion_matrix(test_label, pre_test))
