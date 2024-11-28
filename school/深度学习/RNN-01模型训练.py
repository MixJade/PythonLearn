import tensorflow as tf

# 引入IMDB电影评论数据集
imdb = tf.keras.datasets.imdb
# num_words=10000意为保留训练数据前一万个最常出现的单词
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
# 由于电影评论长度必须相同，我们将使用 pad_sequences 函数来使长度标准化
# post填充:用0向后填充
train_data = tf.keras.preprocessing.sequence.pad_sequences(train_data, padding='post', maxlen=256)
test_data = tf.keras.preprocessing.sequence.pad_sequences(test_data, padding='post', maxlen=256)
print("格式化后的评论长度是:第一条{}，第二条{}".format(len(train_data[0]), len(train_data[1])))
# 建立模型
model = tf.keras.Sequential()
# One-hot过于稀疏，过度占用资源，所以使用embedding
model.add(tf.keras.layers.Embedding(10000, 32))  # 输入形状是用于电影评论的词汇数目（10,000 词）
model.add(tf.keras.layers.LSTM(32))  # 比SimpleRNN更加精细，但是耗时更长
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
# 查看模型各层信息
model.summary()
# 编译模型
model.compile(optimizer='rmsprop',
              loss='binary_crossentropy',
              metrics=['accuracy'])
# 开始训练模型
history = model.fit(train_data,
                    train_labels,
                    epochs=20,
                    batch_size=512,
                    validation_split=0.2,  # 划分验证集
                    )

results = model.evaluate(test_data, test_labels, verbose=2)
print("最终测试损失值{},最终测试精度{}".format(results[0], results[1]))


def draw_history(history01):
    """
    通过训练记录，绘制损失图和精度图

    :param history01:训练的历史记录
    """
    import matplotlib.pyplot as plt

    # 处理历史信息，从中提取出绘制所需的四个属性
    history_dict = history01.history
    print("历史记录的四个条目：", history_dict.keys())
    acc = history_dict['accuracy']
    val_acc = history_dict['val_accuracy']
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    # 开始绘图
    epochs = range(1, len(acc) + 1)
    # “bo”代表 "蓝点"
    plt.plot(epochs, loss, 'bo', label='Training loss')
    # b代表“蓝色实线”
    plt.plot(epochs, val_loss, 'b', label='Validation loss')
    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.show()

    plt.clf()  # 清除数字

    plt.plot(epochs, acc, 'bo', label='Training acc')
    plt.plot(epochs, val_acc, 'b', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()

    plt.show()


draw_history(history)
