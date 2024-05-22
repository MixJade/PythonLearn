# coding=utf-8
# @Time    : 2024/4/15 15:59
# @Software: PyCharm
from base64 import b64encode, b64decode

# noinspection PyPackageRequirements
from Crypto.Cipher import AES, ARC4
# noinspection PyPackageRequirements
from Crypto.Util.Padding import pad, unpad


def pad_key_iv_string(key_bytes: bytes, iv_bytes: bytes) -> tuple[bytes, bytes]:
    """处理输入的密钥、偏移量,
    \n使密钥只有16/24/32位,偏移量只有16位

    :param key_bytes: 密钥的二进制数组
    :param iv_bytes: 偏移量的二进制数组
    """
    pad_key_bytes = "WhatCannotBeSeen".encode()
    pad_iv_bytes = "TimeWaitForNoMan".encode()
    # 先设置key的值
    key_len = len(key_bytes)
    if 32 < key_len:
        key_bytes = key_bytes[:32]
    elif 24 < key_len < 32:
        key_bytes = key_bytes[:24]
    elif 16 < key_len < 24:
        key_bytes = key_bytes[:16]
    elif key_len < 16:
        key_bytes += pad_key_bytes[len(key_bytes):16]
    # 再设置iv的值
    iv_len = len(iv_bytes)
    if 16 < iv_len:
        iv_bytes = iv_bytes[:16]
    elif iv_len < 16:
        iv_bytes += pad_iv_bytes[len(iv_bytes):16]
    # 两个一起返回
    return key_bytes, iv_bytes


def encrypt_text_aes(data: str, key1: bytes, iv1: bytes) -> str:
    """AES的CBC模式加密(只限文本)

    :param data: 明文
    :param key1: 密钥
    :param iv1: 偏移量
    :return: 密文base64文本
    """
    key1, iv1 = pad_key_iv_string(key1, iv1)  # 处理密钥、偏移量
    cipher = AES.new(key1, AES.MODE_CBC, iv1)
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    base64_encrypted = b64encode(ct_bytes)
    return base64_encrypted.decode('utf-8')


def decrypt_text_aes(ciphertext: str, key1: bytes, iv1: bytes) -> str:
    """AES的CBC模式解密(只限文本)

    :param ciphertext: 密文base64文本
    :param key1: 密钥
    :param iv1: 偏移量
    :return: 明文
    """
    try:
        key1, iv1 = pad_key_iv_string(key1, iv1)  # 处理密钥、偏移量
        cipher = AES.new(key1, AES.MODE_CBC, iv1)
        # base64解码为二进制数据
        cipher_byte = b64decode(ciphertext)
        pt = unpad(cipher.decrypt(cipher_byte), AES.block_size)
        # 二进制数据解码为UTF-8明文
        return pt.decode('utf-8')
    except ValueError:
        return "AES解密失败"


def rc4_encrypt(data: str, key1: bytes) -> str:
    """rc4加密"""
    enc = ARC4.new(key1)
    res = enc.encrypt(data.encode('utf-8'))
    res = b64encode(res)
    return res.decode('utf-8')


def rc4_decrypt(ciphertext: str, key1: bytes) -> str:  # 解密
    """rc4解密"""
    ciphertext = b64decode(ciphertext)
    enc = ARC4.new(key1)
    res = enc.decrypt(ciphertext)
    # 二进制数据解码为UTF-8明文
    return res.decode('utf-8')


def encrypt_file(filename: str, key2: bytes, iv2: bytes) -> None:
    """AES加密文件

    :param filename: 明文文件名
    :param key2: 密钥
    :param iv2: 偏移量
    """
    with open(filename, 'rb') as file:
        plaintext = file.read()

    key2, iv2 = pad_key_iv_string(key2, iv2)  # 处理密钥、偏移量
    # AES的CBC模式加密
    cipher = AES.new(key2, AES.MODE_CBC, iv2)
    ct_bytes = cipher.encrypt(pad(plaintext, AES.block_size))
    # 将密文写入新文件
    with open(filename + '.enc', 'wb') as file:
        file.write(ct_bytes)
    print(f'成功加密 {filename} ，加密后文件为 {filename}.enc')


def decrypt_file(filename: str, key2: bytes, iv2: bytes) -> None:
    """AES解密文件

    :param filename: 密文文件名
    :param key2: 密钥
    :param iv2: 偏移量
    """
    with open(filename, 'rb') as file:
        ciphertext = file.read()
    # AES的CBC模式解密
    key2, iv2 = pad_key_iv_string(key2, iv2)  # 处理密钥、偏移量
    cipher = AES.new(key2, AES.MODE_CBC, iv2)
    plain_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # 打印明文
    print(plain_bytes.decode('utf8'))


if __name__ == "__main__":
    key = input("请输入密钥:").encode()
    iv = input("请输入偏移量:").encode()

    while True:
        print("\n-------------------"
              "\nAES加密扣1,AES解密扣2,"
              "\nRC4加密扣4,RC4解密扣5,"
              "\n文件加密扣6,文件解密扣7,"
              "\n重设密钥扣3,终止按0"
              "\n-------------------")
        choose = input("请输入你的选择：")
        # match-case 语法(等于switch)
        match choose:
            case "1":
                plaintext1 = input("输入明文:")
                print(encrypt_text_aes(plaintext1, key, iv))
            case '2':
                ciphertext1 = input("输入密文:")
                print(decrypt_text_aes(ciphertext1, key, iv))
            case '4':
                plaintext1 = input("输入明文:")
                print(rc4_encrypt(plaintext1, key))
            case '5':
                plaintext1 = input("输入密文:")
                print(rc4_decrypt(plaintext1, key))
            case "6":
                plaintext1 = input("输入文件路径:")
                encrypt_file(plaintext1, key, iv)
            case '7':
                ciphertext1 = input("输入文件路径:")
                decrypt_file(ciphertext1, key, iv)
            case '3':
                print(f"当前密钥:{key}\n当前偏移量:{iv}")
                key = input("请输入密钥:").encode()
                iv = input("请输入偏移量:").encode()
            case '0':
                break
