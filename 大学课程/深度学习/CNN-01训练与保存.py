import tensorflow as tf

"""
教材(深度学习之美)上所使用的tensorflow十分的古老,
其版本是Python-3.6,tensorflow-1.7,
许多api现已不支持,而我们要拥抱新技术

当前版本:python-3.9,tensorflow-2.9
"""

# 导入数据集
# noinspection DuplicatedCode
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
