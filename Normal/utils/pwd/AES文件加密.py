# coding=utf-8
# @Time    : 2024/4/16 15:20
# @Software: PyCharm

# noinspection PyPackageRequirements
from Crypto.Cipher import AES
# noinspection PyPackageRequirements
from Crypto.Util.Padding import pad, unpad


def pad_key_iv_string(key_bytes: bytes, iv_bytes: bytes) -> tuple[bytes, bytes]:
    """处理输入的密钥、偏移量,
    \n使密钥只有16/24位,偏移量只有16位

    :param key_bytes: 密钥的二进制数组
    :param iv_bytes: 偏移量的二进制数组
    """
    pad_key_bytes = "WhatCannotBeSeen".encode()
    pad_iv_bytes = "TimeWaitForNoMan".encode()
    # 先设置key的值
    key_len = len(key_bytes)
    if 24 < key_len:
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


def encrypt_file(filename: str, key2: bytes, iv2: bytes) -> None:
    """AES加密文件

    :param filename: 明文文件名
    :param key2: 密钥
    :param iv2: 偏移量
    """
    with open(filename, 'rb') as file:
        plaintext = file.read()

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
    cipher = AES.new(key2, AES.MODE_CBC, iv2)
    plain_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
    # 打印明文
    print(plain_bytes.decode('utf8'))


if __name__ == "__main__":
    key = input("请输入密钥:").encode()
    iv = input("请输入偏移量:").encode()
    key, iv = pad_key_iv_string(key, iv)  # 处理密钥、偏移量
    while True:
        print("\n===加密扣1,解密扣2,重设密钥扣3,终止按0===")
        choose = input("请输入你的选择：")
        # match-case 语法(等于switch)
        match choose:
            case "1":
                plaintext1 = input("输入文件路径:")
                encrypt_file(plaintext1, key, iv)
            case '2':
                ciphertext1 = input("输入文件路径:")
                decrypt_file(ciphertext1, key, iv)
            case '3':
                print(f"当前密钥:{key}\n当前偏移量:{iv}")
                key = input("请输入密钥:").encode()
                iv = input("输入偏移量:").encode()
            case '0':
                break
