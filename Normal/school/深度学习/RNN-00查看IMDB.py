import tensorflow as tf

# 引入IMDB电影评论数据集(训练集测试集各25000个评论)
imdb = tf.keras.datasets.imdb
# num_words=10000意为保留训练数据前一万个最常出现的单词
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
# 查看部分相关参数
print("训练集有: {}个, 训练标签有: {}个".format(len(train_data), len(train_labels)))
print("测试集有: {}个, 测试标签有: {}个".format(len(test_data), len(test_labels)))
print("它的评论数据长这样:\n", train_data[0])
print("第一条评论的长度为:{},第二条评论的长度为:{}".format(len(train_data[0]), len(train_data[1])))


def decode_review(text):
    """
    将数据变回英文评论
    """
    word_index = imdb.get_word_index()  # 一个映射单词到整数索引的词典
    # 保留第一个索引
    word_index = {k: (v + 3) for k, v in word_index.items()}
    word_index["<PAD>"] = 0
    word_index["<START>"] = 1
    word_index["<UNK>"] = 2  # unknown
    word_index["<UNUSED>"] = 3
    reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
    return ' '.join([reverse_word_index.get(i, '?') for i in text])


def save_comment():
    """
    将评论解码并保存为txt文件
    """
    file = '../A2兼收并蓄/电影评论.txt'
    file_object = open(file, "w+")
    file_object.write(decode_review(train_data[0]))
    print("第一条评论已成功写入文件" + file)

# save_comment
