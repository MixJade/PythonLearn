# RNN学习过程的废案.md

> 学习过程中所淘汰的代码，为了避免误解放在这里

**目录**:

1. [RNN官网代码](#RNN官网代码)
2. [关于Bug：libiomp5md.dll存在多个](#关于Bug：libiomp5md.dll存在多个)

# RNN官网代码
* 这是从官网上取下来，进行语法上改良的代码
* 它与老师提供的代码不同之处:
    * 在输入层(Embedding)到输出层之间，它使用的是矩阵平均池化层 + 16神经元使用relu函数的全连接层
    * 而老师用的是SimpleRNN层（后面优化为LSTM层）
    * 它输入数据批数为16，老师的是32，事实上这个影响不大
    * 它所用优化器为adam，老师的是rmsprop

* RNN-01模型训练官网.py

```python
import tensorflow as tf

# 引入IMDB电影评论数据集
imdb = tf.keras.datasets.imdb
# num_words=10000意为保留训练数据前一万个最常出现的单词
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
# 由于电影评论长度必须相同，我们将使用 pad_sequences 函数来使长度标准化
# post填充:用0向后填充
train_data = tf.keras.preprocessing.sequence.pad_sequences(train_data,
                                                           padding='post',
                                                           maxlen=256)
test_data = tf.keras.preprocessing.sequence.pad_sequences(test_data,
                                                          padding='post',
                                                          maxlen=256)
print("格式化后的评论长度是:第一条{}，第二条{}".format(len(train_data[0]), len(train_data[1])))

model = tf.keras.Sequential()
# One-hot的缺点：过于稀疏，过度占用资源，所以我们使用embedding
# embedding的原理是使用矩阵乘法来进行降维，从而达到节约存储空间的目的
# 比如2行6列的信息 乘 6行3列的矩阵，就变成2行3列的矩阵（降维）
model.add(tf.keras.layers.Embedding(10000, 16))  # 输入形状是用于电影评论的词汇数目（10,000 词）
model.add(tf.keras.layers.GlobalAveragePooling1D())  # 矩阵平均池化
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))
# 编译模型
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
# 开始训练模型
# verbose=1默认值，意思是输出进度条记录，为0就是不输出记录
# validation_split的意思是划分训练集，这里是划分最后20%，即后5000个
history = model.fit(train_data[10000:],
                    train_labels[10000:],
                    epochs=20,
                    batch_size=512,
                    validation_split=0.2,
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

```

## 关于Bug：libiomp5md.dll存在多个

* 具体表现为：画图时画不出来，并报错`OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.`

* 解决方法：
* 去anaconda3目录搜索libiomp5md.dll
* anaconda3就在用户目录下


