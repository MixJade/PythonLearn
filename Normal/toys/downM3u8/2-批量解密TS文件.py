# coding=utf-8
# @Time    : 2024/8/23 22:49
# @Software: PyCharm
import os

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


# 解密操作
def decrypt(key, encrypted_ts_directory, decrypt_ts_directory):
    # AES对象，传入密钥，偏移量，模式
    # key必须为字节
    aes = AES.new(key=key, IV=b'0000000000000000', mode=AES.MODE_CBC)
    # 获取文件或目录列表（返回的list的顺序跟我们想要的不一样）
    ts_all = os.listdir(encrypted_ts_directory)
    for ts in ts_all:
        if not ts.endswith(".ts"):
            continue
        with open(file=encrypted_ts_directory + f'/{ts}', mode='rb') as fr:
            with open(file=decrypt_ts_directory + f'/{ts}', mode='wb') as fw:
                # 从加密的文件夹中读取文件
                encrypted_data = fr.read()
                # 获取长度
                encrypted_data_len = len(encrypted_data)
                # 判断当前的数据长度是不是16的倍数
                if encrypted_data_len % 16 != 0:
                    # 把长度不是16的倍数的显示出来
                    # print(encrypted_data_len)
                    # 变为16的倍数
                    encrypted_data = pad(encrypted_data, 16)
                # 进行解密
                decrypt_data = aes.decrypt(encrypted_data)
                # 将解密后的数据写入对应的解密文件
                fw.write(decrypt_data)
    print('解密成功！')


# downM3u8文件夹路径(假定刚执行过`1-下载m3u8文件.py`)
input_dir = "../../outputFile/downM3u8/"
# 输出文件夹
out_put_dir = "../../outputFile/downM3u8-2/"
# 新建一个文件夹用于存放.ts文件
if not os.path.exists(out_put_dir):
    os.mkdir(out_put_dir)

print("开始解密")

with open(input_dir + 'key.dat', 'r') as f_data:
    scale = 16  # 16进制
    num_of_bits = 8
    hex_content = f_data.read().strip()  # 读取文件内容并删除两边的空格或换行
    print(hex_content)
    decrypt(hex_content.encode('utf-8'), input_dir, out_put_dir)
