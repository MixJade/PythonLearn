# CNN学习过程的废案

* 过期书本害人不浅，我相信书上的代码，结果那个代码过期四年了
* 我以为是因为版本更新，特意去把那些api的变更给找了一遍
* 但是训练效果还是微不足道，为此足足耗了我两天时间
* 直到我找到了tensorflow的官网，十分钟就整出来了

附上[tensorflow的官网](https://tensorflow.google.cn/learn)

还是要看官网啊

## 加载MNIST数据集

> 从MNIST的官网上下载的四个数据集
> 因为解析的包我没有找到就自己写了一个

* 加载MNIST数据集.py
* 注: MNIST文件下载地址:http://yann.lecun.com/exdb/mnist/

```python
import numpy as np
import gzip

"""
定义加载数据的函数，data_path为保存gz数据的文件夹，该文件夹下有4个文件
'train-labels-idx1-ubyte.gz', 'train-images-idx3-ubyte.gz',
't10k-labels-idx1-ubyte.gz', 't10k-images-idx3-ubyte.gz'

注: MNIST文件下载地址:http://yann.lecun.com/exdb/mnist/
注: 为了美观，文件夹记得放在这个py文件夹的同级，并在pycharm中打上"已排除"
"""


def load_data(data_path):
    """
    加载MNIST数据集

    :param data_path: MNIST在电脑上的存放路径
    :return: MNIST的四个元组
    """
    # 训练集标签
    with gzip.open(data_path + 'train-labels-idx1-ubyte.gz', 'rb') as lbpath:
        y_train = np.frombuffer(lbpath.read(), np.uint8, offset=8)
        y_train_onehot = np.eye(10)[y_train]  # 转化成独热编码
    # 训练集图片
    with gzip.open(data_path + 'train-images-idx3-ubyte.gz', 'rb') as imgpath:
        x_train = np.frombuffer(
            imgpath.read(), np.uint8, offset=16).reshape(len(y_train), 28, 28, 1)

    # 测试集标签
    with gzip.open(data_path + 't10k-labels-idx1-ubyte.gz', 'rb') as lbpath:
        y_test = np.frombuffer(lbpath.read(), np.uint8, offset=8)
        y_test_onehot = np.eye(10)[y_test]  # 转化成独热编码
    # 测试集图片
    with gzip.open(data_path + 't10k-images-idx3-ubyte.gz', 'rb') as imgpath:
        x_test = np.frombuffer(
            imgpath.read(), np.uint8, offset=16).reshape(len(y_test), 28, 28, 1)

    return (x_train, y_train_onehot), (x_test, y_test_onehot)


def next_batch(train_data, train_target, batch_size):
    """
    随机取指定数量的数据

    :param train_data: 训练样本
    :param train_target: 训练标签
    :param batch_size: 所取数据数量
    :return: 随机数量的训练样本及其标签
    """
    # 打乱数据集
    index = [i for i in range(0, len(train_target))]
    np.random.shuffle(index)
    # 建立batch_data与batch_target的空列表
    batch_data = []
    batch_target = []
    # 向空列表加入训练集及标签
    for i in range(0, batch_size):
        batch_data.append(train_data[index[i]])
        batch_target.append(train_target[index[i]])
    return batch_data, batch_target  # 返回


def drawing(batch01):
    """
    绘制所选取的训练集图片

    :param batch01: 随机选取训练集样本及标签
    """
    import matplotlib.pyplot as plt

    n_samples = len(batch01[1])  # 需要输出图片的数量
    # 输出图片的实际数字
    data = [np.argmax(one_hot) for one_hot in batch01[1]]  # 将独热编码转换成数字
    print(data)  # 所选择的图片实际数字
    # 输出图片
    plt.figure(figsize=(n_samples * 2, 3))
    for n_index in range(n_samples):
        plt.subplot(1, n_samples, n_index + 1)
        sample_image = batch01[0][n_index]
        plt.imshow(sample_image, cmap="binary")
        plt.axis("off")
    plt.show()  # 所选择的图片


if __name__ == '__main__':
    # 加载MNIST数据集
    (train_images, train_labels), (test_images, test_labels) = load_data('MNIST数据集/')
    print("训练集样本及标签", train_images.shape, train_labels.shape)
    print("测试集样本及标签", test_images.shape, test_labels.shape)
    # 随机获取数据
    batch = next_batch(train_images, train_labels, 5)
    # 绘制图片
    drawing(batch)
```

tf_upgrade_v2 --infile CNN第一版本.py --outfile first-tf-v2.py

## CNN第一版本

* 课本上的代码，过时4年了
* 所幸。tensorflow仍然保留着
* 但是无论是运行效率，还是编程效率，都远远不如2.0的框架化

* CNN第一版本.py

```python
# import tensorflow as tf  # 太超前导致不兼容
import tensorflow._api.v2.compat.v1 as tf
from 加载MNIST数据集 import load_data
from 加载MNIST数据集 import next_batch

"""
本代码脱胎于书P480，但是更新了许多地方(比如几个过时的函数)
注释写的比代码多(bushi)
注: 加载MNIST数据集是自己写的，可以跳转过去看源码
注: MNIST文件下载地址:http://yann.lecun.com/exdb/mnist/
"""
tf.disable_eager_execution()  # 禁用急切执行，从此使用会话来获取操作结果
mnist = load_data('MNIST数据集/')  # 这个是存放MNIST的文件夹，自己写
(train_images, train_labels), (test_images, test_labels) = mnist
train_images, test_images = train_images / 255.0, test_images / 255.0


def weight_variable(shape):
    """
    初始化权值

    :param shape: [宽，高，输入通道数，输出通道数]or[每个神经元训练次数，神经元个数]
    :return: 权值
    """
    initial = tf.truncated_normal(shape, stddev=0.1)  # 截断正态分布函数来产生权值，标准方差为0.1
    return tf.Variable(initial)  # 创建tensor类型的变量


def bias_variable(shape):
    """
    初始化偏置

    :param shape: 偏置元素个数(输出通道or神经元)
    :return: 偏置变量
    """
    initial = tf.constant(0.1, shape=shape)  # 形状为shape，数值为0.1的常量
    return tf.Variable(initial)  # 创建tensor类型的变量


def conv2d(x1, w):
    """
    卷积核

    :param x1: 图像
    :param w: 权值
    :return: 卷积结果
    """
    return tf.nn.conv2d(x1, w, strides=[1, 1, 1, 1], padding='SAME')  # 布幅为1，零值等大填充


def max_pool_2x2(x2):
    """
    池化操作

    :param x2: 卷积效果(卷积结果+偏置,再通过Relu激活)
    :return: 池化结果
    """
    return tf.nn.max_pool(x2, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')  # 最大值池化，池化核形状2x2,在水平和垂直方向上步长为2


# 定义输入的参数
x = tf.placeholder(tf.float32, [None, 28, 28, 1])  # 占位符定义外部输入数据,
y_ = tf.placeholder(tf.float32, [None, 10])  # 占位符存放标签
# x_image = tf.reshape(x, [-1, 28, 28, 1])  # 将输入的1x784变成28x28,-1表示样本数量不定,1表示单通道(黑白图片)

# 开始构建卷积层
W_conv1 = weight_variable([5, 5, 1, 32])  # 卷积核大小5x5,单通道,32个输出通道(即32个特征)
b_conv1 = bias_variable([32])  # 偏置变量,32个元素(每个输出通道配一个)
h_conv1 = tf.nn.relu(conv2d(x, W_conv1) + b_conv1)  # 卷积结果加上偏置，通过Relu激活函数，得到卷积效果(不是结果)
h_pool1 = max_pool_2x2(h_conv1)  # 为了防止过拟合，进行最大值池化

# 第二个卷积层
W_conv2 = weight_variable([5, 5, 32, 64])  # 32个输入,64个输出
b_conv2 = bias_variable([64])  # 偏置变量64个元素
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# 实现全连接层
# 此时前面经过两个2x2的最大值池化,图像维度缩减1/4,变成7x7
W_fc1 = weight_variable([7 * 7 * 64, 1024])  # 图像乘64个通道(与第二个卷积输出匹配)即每个神经元训练次数,1024个神经元
b_fc1 = bias_variable([1024])  # 偏置变量1024个元素
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])  # 将第二个卷积的4D矩阵变成1D,-1表示不限样本数(与样本数一致)
# matmul是矩阵乘法，即卷积层输出结果x权值矩阵+偏置变量，最后通过Relu激活
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)  # 全连接层输出张量

# 实现Dropout层
# 防止全连接层过多的参数导致过拟合
keep_prob = tf.placeholder(tf.float32)  # 占位符
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  # keep_prob保留概率，为1就是全部保留

# 实现Readout层,即Softmax回归层
# 得到分类概率
W_fc2 = weight_variable([1024, 10])  # 1024对应全连接层,10个神经元分布输出每个数字的概率
b_fc2 = bias_variable([10])  # 对应10个神经元
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2  # 逻辑回归

# 参数训练与模型评估
# tf.reduce_mean表示从一批(batch)数据中求均值,tf.nn.softmax_cross_entropy_with_logits为交叉熵函数(作为损失函数)
# 损失函数(交叉熵)
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.math.log(y_conv), 1))
# 优化器
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
# 计算模型精度
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# 建立一个交互式会话
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())
for i in range(301):
    batch = next_batch(train_images, train_labels, 50)
    if i % 50 == 0:
        train_accuracy = accuracy.eval(feed_dict={
            x: batch[0], y_: batch[1], keep_prob: 1.0})
        print('step %d, 训练精度为 %g' % (i, train_accuracy))
    # 训练时的Dropout层，概率为0.5
    sess.run(train_step, feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})
test_accuracy = accuracy.eval(feed_dict={
    x: test_images, y_: test_labels, keep_prob: 1.0})
print('测试精度 %g' % test_accuracy)

sess.close()

```

# CNN第二版本.py

* CNN的2.0版本
* 主要是使用一些没有被废弃的函数
* 但还是不如框架化

```python
import tensorflow as tf
from 加载MNIST数据集 import load_data
from 加载MNIST数据集 import next_batch

"""
第一代代码的改进
主要是为了贴合tansorflow2.0的更新
但是，事实证明，贴合的不够，
人家已经全面起飞了，我还在骑自行车
"""
mnist = load_data('MNIST数据集/')  # 这个是存放MNIST的文件夹，自己写
(train_images, train_labels), (test_images, test_labels) = mnist
train_images, test_images = train_images / 255.0, test_images / 255.0


def weight_variable(shape):
    """
    初始化权值

    :param shape: [宽，高，输入通道数，输出通道数]or[每个神经元训练次数，神经元个数]
    :return: 权值
    """
    initial = tf.random.truncated_normal(shape, stddev=0.1)  # 截断正态分布函数来产生权值，标准方差为0.1
    return tf.Variable(initial)  # 创建tensor类型的变量


def bias_variable(shape):
    """
    初始化偏置

    :param shape: 偏置元素个数(输出通道or神经元)
    :return: 偏置变量
    """
    initial = tf.constant(0.1, shape=shape)  # 形状为shape，数值为0.1的常量
    return tf.Variable(initial)  # 创建tensor类型的变量


def conv2d(x1, w):
    """
    卷积核

    :param x1: 图像
    :param w: 权值
    :return: 卷积结果
    """
    return tf.nn.conv2d(x1, w, strides=[1, 1, 1, 1], padding='SAME')  # 布幅为1，零值等大填充


def max_pool_2x2(x2):
    """
    池化操作

    :param x2: 卷积效果(卷积结果+偏置,再通过Relu激活)
    :return: 池化结果
    """
    return tf.nn.max_pool(x2, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding='SAME')  # 最大值池化，池化核形状2x2,在水平和垂直方向上步长为2


"""
网络构建从此开始
"""

w_conv1 = weight_variable([5, 5, 1, 32])  # 卷积核大小5x5,单通道,32个输出通道(即32个特征)
b_conv1 = bias_variable([32])  # 偏置变量,32个元素(每个输出通道配一个)


def roll_01(x_01):
    """
    第一个卷积层

    :param x_01: 一批图像
    :return: h_pool1
    """
    h_conv1 = tf.nn.relu(conv2d(x_01, w_conv1) + b_conv1)  # 卷积结果加上偏置，通过Relu激活函数，得到卷积效果(不是结果)
    h_pool1 = max_pool_2x2(h_conv1)  # 为了防止过拟合，进行最大值池化
    return h_pool1


w_conv2 = weight_variable([5, 5, 32, 64])  # 32个输入,64个输出
b_conv2 = bias_variable([64])  # 偏置变量64个元素


def roll_02(h_pool1):
    """
    第二个卷积层

    :param h_pool1: 第一卷积层返回值
    :return: h_pool2
    """
    h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)
    return h_pool2


w_fc1 = weight_variable([7 * 7 * 64, 1024])  # 图像乘64个通道(与第二个卷积输出匹配)即每个神经元训练次数,1024个神经元
b_fc1 = bias_variable([1024])  # 偏置变量1024个元素


def full_link(h_pool2):
    """
    实现全连接层

    :param h_pool2: 第二个卷积层返回值
    :return: h_fc1
    """
    # 此时前面经过两个2x2的最大值池化,图像维度缩减1/4,变成7x7
    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])  # 将第二个卷积的4D矩阵变成1D,-1表示不限样本数(与样本数一致)
    # matmul是矩阵乘法，即卷积层输出结果x权值矩阵+偏置变量，最后通过Relu激活
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)  # 全连接层输出张量
    return h_fc1


def drop(keep_prob, h_fc1):
    """
    实现Dropout层

    :param keep_prob: 保留概率
    :param h_fc1: 全连接层输出张量
    :return: h_fc1_drop
    """
    # 防止全连接层过多的参数导致过拟合
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)  # keep_prob保留概率
    return h_fc1_drop


w_fc2 = weight_variable([1024, 10])  # 1024对应全连接层,10个神经元分布输出每个数字的概率
b_fc2 = bias_variable([10])  # 对应10个神经元


def readout(h_fc1_drop):
    """
    实现Readout层,
    即Softmax回归层,
    得到分类概率

    :param h_fc1_drop: Dropout层输出
    :return: y_conv
    """
    y_conv = tf.matmul(h_fc1_drop, w_fc2) + b_fc2  # 逻辑回归
    return y_conv


def loss(y0, y_conv):
    """
    损失函数(交叉熵)

    :param y0: 训练样本标签
    :param y_conv: 网络实际输出
    :return: cross_entropy
    """
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(labels=y0, logits=y_conv)
    return cross_entropy


def before_drop(x0):
    """
    在dropout层之前的输出

    :param x0: 将图片注入网络
    :return: h_fc1
    """
    x0 = tf.convert_to_tensor(x0, tf.float32)
    h_pool1 = roll_01(x0)
    h_pool2 = roll_02(h_pool1)
    h_fc1 = full_link(h_pool2)
    return h_fc1


@tf.function
def cnn_out(x0, keep_prob):
    """
    对神经网络进行一个单向的输出

    :param x0:  将图片注入网络
    :param keep_prob: drop_out层保留神经元概率
    :return: 网络实际输出
    """
    h_fc1 = before_drop(x0)
    h_fc1_drop = drop(keep_prob, h_fc1)
    y_conv = readout(h_fc1_drop)
    return y_conv


def precision(x0, y0):
    """
    计算模型精度

    :return: 模型精度评估
    """
    h_fc1 = before_drop(x0)
    y_conv = readout(h_fc1)
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y0, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    return accuracy


# 优化器,优化寂寞
train_step = tf.optimizers.Adam(0.1)

for i in range(201):
    batch = next_batch(train_images, train_labels, 50)
    with tf.GradientTape(persistent=True) as t:
        # 训练时的Dropout层，概率为0.5
        y_out = cnn_out(x0=batch[0], keep_prob=0.5)
        list_var = [w_conv1, b_conv1, w_conv2, b_conv2, w_fc1, b_fc1, w_fc2, b_fc2]
        loss_current = loss(y0=batch[1], y_conv=y_out)
        grads = t.gradient(target=loss_current, sources=list_var)
        train_step.apply_gradients(zip(grads, list_var))
    if i % 50 == 0:
        train_accuracy = precision(x0=batch[0], y0=batch[1])
        print('step %d, 训练精度为 %g' % (i, train_accuracy))

test_accuracy = precision(x0=test_images, y0=test_labels)
print('测试精度 %g' % test_accuracy)

```