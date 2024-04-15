# coding=utf-8
# @Time    : 2024/4/15 17:05
# @Software: PyCharm
from unittest import TestCase

from utils.pwd.加解密工具 import encrypt_text_aes, decrypt_text_aes

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
