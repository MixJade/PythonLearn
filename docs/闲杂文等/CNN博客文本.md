# 基于CNn的MINIST手写体识别

> 深度学习的上机作业:
> * 基于CNN卷积神经网络的MINIST手写体识别
> * 版本:python-3.9,tensorflow-2.9

**目录**:

1. [MINIST数据集](#MINIST数据集)
2. [训练CNN卷积神经网络](#训练CNN卷积神经网络)
3. [使用训练好的模型进行预测](#使用训练好的模型进行预测)
4. [识别自己手写的数字](#识别自己手写的数字)

写这篇文章为了讲一个故事：

老师布置了一个上机作业，建议参照着书上的代码进行完成， 但书上的代码是四年前的，tensorflow已经大变样了， 然后我浪费了两天的时间来改Bug与兼容，最终选择照着官方文档写2.0-tensorflow的故事。

---

## MINIST数据集

> 由很多人手写的数字构成,分为训练集与测试集

**训练集**: 有6万张图片,每张图片大小28x28,同时有对应数量的标签(就是每张图片对应的数字)

**测试集**: 与训练集相比,其他一样，就是图片只有1万张

我们可以看看测试集的大小与部分图片

**代码**:

```python
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
```

运行结果:

* 数据集大小:
* 图像:

---

## 训练CNN卷积神经网络

> 如果看这篇文章是为了完成实验报告，就用这里的代码就行

这个代码是不是看着比书(深度学习之美)上的示例代码简洁？这就是tensorflow在四年的发展， 它从原来的偏向底层的代码变成现在这种高度集成的框架，但没有书上那样可以清楚的知道底层是如何实现的。

我将讲解这个代码所定义的神经网络模型，

(与书上唯一不同的就是全连接层的神经元为64个)。

1. 第一层为卷积层,32卷积核(即32输出通道),卷积核大小5x5,激活函数Relu,零值等大填充
2. 第二层为池化层，2x2最大值池化
3. 第三层为卷积层，卷积核大小5x5，64个输出通道
4. 第四层为池化层，仍为2x2最大池化
5. 第五层为扁平化层，将输入的二维张量拉成一维，便于输入给全连接层
6. 第六层为全连接层，与书上不同，这里是64个神经元(因为我的电脑内存不大)
7. 第七层为Dropout层，随机丢掉一些全连接层的神经元，以避免过拟合
8. 第八层，即最后一层，为输出层，输出独热编码

**代码**：（最后一行是自己的文件路径）

```python
import tensorflow as tf

"""
教材(深度学习之美)上所使用的tensorflow十分的古老,
其版本是Python-3.6,tensorflow-1.7,
许多api现已不支持,而我们要拥抱新技术

当前版本:python-3.9,tensorflow-2.9
"""

# 导入数据集
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
print("训练集样本及标签", train_images.shape, train_labels.shape)
print("测试集样本及标签", test_images.shape, test_labels.shape)
train_images, test_images = train_images / 255.0, test_images / 255.0  # 归一化,不然梯度爆炸

# 建立各层神经网络
model = tf.keras.models.Sequential()  # 建立一个堆叠层的神经网络
# 第一卷积层,32卷积核(即32输出通道),卷积核大小5x5,使用Relu激活函数,零值等大填充,输入张量形状28x28,色彩通道为1(即黑白图片)
model.add(tf.keras.layers.Conv2D(32, (5, 5), activation='relu', padding='same', input_shape=(28, 28, 1)))
# 2x2的最大值池化
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
# 第二卷积层,64个输出通道，输入通道这里就不用指定，可以自动承接前一层的
model.add(tf.keras.layers.Conv2D(64, (5, 5), activation='relu', padding='same'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
# 扁平化,将二维的张量变成一维,这里28x28经过两次2x2池化,已是7x7大小,现在变成49
model.add(tf.keras.layers.Flatten())
# 全连接层,64个神经元
model.add(tf.keras.layers.Dense(64, activation='relu'))
# dropout层，损失函数0.5
model.add(tf.keras.layers.Dropout(0.5))
# Readout层，输出独热编码
model.add(tf.keras.layers.Dense(10))  # 最后输出10个数

# 编译模型
model.compile(optimizer='adam',  # Adam优化器
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # 损失函数
              metrics=['accuracy'])  # 监控指标:精度
# 开始训练,训练周期8,即将所有训练样本(6万个),遍历八遍,因为输入通道是32个,所以每遍训练1875次,每次32个
model.fit(train_images, train_labels, epochs=8, validation_data=(test_images, test_labels))

# 训练完毕，使用测试集来评估模型精度
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print('\n最终测试集上的精度为:', test_acc)

# 保存模型
model.save("../A2兼收并蓄/CNN模型")  # 这是自定义的路径,删除"/A2兼收并蓄"即可直接运行

```

**运行结果**:在训练集上训练了1875x8=15000次，每次32张图片，最终在测试集上的精度为: 0.9926

---

## 使用训练好的模型进行预测

好不容易将模型训练完了，怎么能够不去使用？

从文件夹读取出模型，开始预测，看看自己亲手训练出的成果如何。

（这里应该将图片给显示出来才直观，但是那样意义不大，只看标签也够了）

**代码**:

```python
import tensorflow as tf

# 导入数据集
mnist = tf.keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# 引入模型
model = tf.keras.models.load_model("../A2兼收并蓄/CNN模型")
# 加入待预测的图像及其标签
show_images, show_labels = test_images[0:20], test_labels[0:20]
print("所选取的测试集图片的标签is:", show_labels)
# 开始预测
predictions = model.predict(show_images)
# 预测完成,预测结果是类似独热编码的形式(10个标签的概率)
# 将预测结果通过取最大值的下标的形式变成预测结果
predictions_num = tf.argmax(predictions, 1)
# 输出所预测的标签
print("所预测的标签为:", predictions_num)

```

**运行结果**：（可以看到训练20个图像，全部都预测对了）

---

## 识别自己手写的数字

> 好不容易训练的模型，应该自己体验一番，自己画一个数字，看看是否能够识别

* 首先打开画图，将图像设置为28x28的黑白图像（打开画图-->文件-->图像属性）（其实不设也行，但那样不能保证精度）
* 然后画一个黑底白字的数字，保存为png文件（我这里起名“御笔亲题之作”）
* （这个时候可能看不清画布，用画图的放大镜点几下就好了）
* 然后通过tf.io进行读取，并转化成numpy数组

代码：

```python
import tensorflow as tf

# 读取一张自己手写的图片，并将之转化成28x28的numpy数组
img_01 = tf.io.read_file("../A2兼收并蓄/御笔亲题之作.png")  # 要黑白图片
img02 = tf.io.decode_png(img_01, channels=1)  # 图像通道为1,读取黑白图片
img03 = tf.image.resize(img02, [28, 28])  # 保险起见,将图片大小强行变成28x28
img = (img03.numpy()).reshape([1, 28, 28])  # 转化成28x28的numpy数组
print("图片转化之后的形状为:", img.shape)
# 运用模型进行预测
model = tf.keras.models.load_model("../A2兼收并蓄/CNN模型")
predictions = model.predict(img)
predictions_num = tf.argmax(predictions, 1)
print("你的模型认为该数字为:", predictions_num.numpy())

```

运行结果:
你的模型认为该数字为: [7]

---