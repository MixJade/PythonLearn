# coding=utf-8
# @Time    : 2024/4/15 15:59
# @Software: PyCharm
import base64
from base64 import b64encode

# noinspection PyPackageRequirements
from Crypto.Cipher import AES
# noinspection PyPackageRequirements
from Crypto.Util.Padding import pad
# noinspection PyPackageRequirements
from Crypto.Util.Padding import unpad


def pad_key_string(input_bytes: bytes) -> bytes:
    """对输入的密钥进行处理，输出长度为16、24、32的数组"""
    if len(input_bytes) < 24:
        # 输出的数组长度小于24，则输出16位的密钥
        return pad_iv_string(input_bytes)
    elif 24 < len(input_bytes) < 32:
        # 输出数组的长度大于24但小于32，则输出24位数组
        return input_bytes[:24]
    elif len(input_bytes) > 32:
        # 输出数组的长度大于32，则输出32位数组
        return input_bytes[:32]
    else:
        return input_bytes


def pad_iv_string(input_bytes: bytes) -> bytes:
    """对输入的偏移量进行处理，输出长度为16数组"""
    pad_bytes = "TimeWaitForNoMan".encode()
    if len(input_bytes) < 16:
        return input_bytes + pad_bytes[len(input_bytes):16]
    elif len(input_bytes) > 16:
        return input_bytes[:16]
    else:
        return input_bytes


def encrypt_text_aes(data: str, key1: bytes, iv1: bytes) -> str:
    """AES的CBC模式加密(只限文本)

    :param data: 明文
    :param key1: 密钥
    :param iv1: 偏移量
    :return: 密文base64文本
    """
    key1, iv1 = pad_key_string(key1), pad_iv_string(iv1)
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
    key1, iv1 = pad_key_string(key1), pad_iv_string(iv1)
    cipher = AES.new(key1, AES.MODE_CBC, iv1)
    # base64解码为二进制数据
    cipher_byte = base64.b64decode(ciphertext)
    pt = unpad(cipher.decrypt(cipher_byte), AES.block_size)
    # 二进制数据解码为UTF-8明文
    return pt.decode('utf-8')


if __name__ == "__main__":
    key = input("请输入密钥:").encode()
    iv = input("请输入偏移量:").encode()

    while True:
        print("\n===加密扣1,解密扣2,重设密钥扣3,终止按0===")
        choose = input("请输入你的选择：")
        # match-case 语法(等于switch)
        match choose:
            case "1":
                plaintext1 = input("输入明文:")
                print(encrypt_text_aes(plaintext1, key, iv))
            case '2':
                ciphertext1 = input("输入密文:")
                print(decrypt_text_aes(ciphertext1, key, iv))
            case '3':
                print(f"当前密钥:{key}\n当前偏移量:{iv}")
                key = input("请输入密钥:").encode()
                iv = input("请输入偏移量:").encode()
            case '0':
                break
