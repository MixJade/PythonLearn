import tensorflow as tf

# 读取一张自己手写的图片，并将之转化成28x28的numpy数组
img_01 = tf.io.read_file("../A1输入数据/御笔亲题之作.png")  # 要黑白图片
img02 = tf.io.decode_png(img_01, channels=1)  # 图像通道为1,读取黑白图片
img03 = tf.image.resize(img02, [28, 28])  # 保险起见,将图片大小强行变成28x28
img = (img03.numpy()).reshape([1, 28, 28])  # 转化成28x28的numpy数组
print("图片转化之后的形状为:", img.shape)
# 运用模型进行预测
model = tf.keras.models.load_model("../A2兼收并蓄/CNN模型")
predictions = model.predict(img)
predictions_num = tf.argmax(predictions, 1)
print("你的模型认为该数字为:", predictions_num.numpy())
