# Python中英文混排对齐

> 2024-09-17 11:39:02

## 一、纯中文对齐

* 参考链接：[python中英文混排格式化输出](https://zhuanlan.zhihu.com/p/519003659)

在填充字段使用`chr(12288)`这个中文空格符进行填充即可

这里我们修改print语句，在占位宽度前面加上`chr(12288)}`代表用中文空格填充。

* 样例

```python
print(f"文件: {f:{chr(12288)}<20}修改时间: {mod_time}")
```

## 二、中英文混合对齐

* 参考链接: [python中英文混合字符串对齐-CSDN](https://blog.csdn.net/f__yuan/article/details/117994930)

主要是逐个字符解析，区别是中文还是英文

中文占两个字符,英文占一个,所以最终长度应该为(总长度-中文数)

```python
# coding=utf-8
# @Time    : 2024/9/17 11:37
# @Software: PyCharm

def align_text(title_str: str, max_len: int) -> str:
    """返回加入了占位符的文字
    
    :param title_str: 需要处理的中英文混合字符串
    :param max_len: 格式化后的最大长度(按英文空格计数)
    :return: 最终格式化后的字符串
    """
    for j in str(title_str):
        if '\u4e00' <= j <= '\u9fff':
            max_len = max_len - 1
    # 中文占两个字符,英文占一个,所以最终长度应该为(总长度-中文数)
    # 左对齐,并填充字符串
    return title_str.ljust(max_len, ' ')
```

