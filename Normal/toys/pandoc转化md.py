# coding=utf-8
# @Time    : 2024/6/11 21:57
# @Software: PyCharm
import subprocess

command = [
    'pandoc',
    'input.md',
    '-o', 'output.epub',
]

subprocess.run(command, check=True)
