import tensorflow as tf
import matplotlib.pyplot as plt

# 导入数据集
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print("训练集样本及标签", train_images.shape, train_labels.shape)
print("测试集样本及标签", test_images.shape, test_labels.shape)
train_images, test_images = train_images / 255.0, test_images / 255.0  # 归一化,不然梯度爆炸
# 进行绘画
for i in range(15):
    plt.subplot(3, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(test_images[i])
    plt.xlabel(test_labels[i])
plt.show()
