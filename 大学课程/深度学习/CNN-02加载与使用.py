import tensorflow as tf

# 导入数据集
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# 加入待预测的图像及其标签
show_images, show_labels = test_images[0:20], test_labels[0:20]
print("所选取的测试集图片的标签is:", show_labels)
# 引入模型
model = tf.keras.models.load_model("../A2兼收并蓄/CNN模型")
# 开始预测
predictions = model.predict(show_images)
# 预测完成,预测结果是类似独热编码的形式(10个标签的概率)
# 将预测结果通过取最大值的下标的形式变成预测结果
predictions_num = tf.argmax(predictions, 1)
# 输出所预测的标签
print("所预测的标签为:", predictions_num)
