# coding=utf-8
# @Time    : 2024/4/15 17:05
# @Software: PyCharm
from unittest import TestCase

from utils.加解密工具 import encrypt_text_aes, decrypt_text_aes, rc4_encrypt, rc4_decrypt

# 测试的密钥与偏移量
key = 'WhatCannotBeSeen'.encode()
iv = 'TimeWaitForNoMan'.encode()


# noinspection SpellCheckingInspection
class TestAES(TestCase):
    def test_encrypt_text_aes(self):
        # 测试加密
        result = encrypt_text_aes("Hello World", key, iv)
        self.assertEqual("7R+CSqAcl/OKRRCGxzZ1ig==", result)

    def test_decrypt_text_aes(self):
        # 测试解密
        result = decrypt_text_aes("7R+CSqAcl/OKRRCGxzZ1ig==", key, iv)
        self.assertEqual("Hello World", result)

    def test_rc4_encrypt(self):
        # 测试rc4加密
        result = rc4_encrypt("你好世界", key)
        self.assertEqual("9D/3uDvPv7Z9rhVf", result)

    def test_rc4_decrypt(self):
        # 测试rc4解密
        result = rc4_decrypt("9D/3uDvPv7Z9rhVf", key)
        self.assertEqual("你好世界", result)
