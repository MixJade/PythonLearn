# Python字符串语法糖

> 2024年2月12日14:26:31

Python的几种字符串语法糖包括：

1. `f"..."` ：f-string 格式化字符串，用于插入并格式化字符串中的表达式。表达式在 `{}` 中，可以在其中使用变量，函数等。

例子：
```python
name = "Alice"
print(f"Hello, {name}")  # 输出：Hello, Alice
```

2. `r"..."` ：原始字符串，所有的字符串都是直接按照字面的意思来使用，没有转义特殊或不能打印的字符。

例子：
```python
print(r"
")  # 输出：

```

3. `b"..."` ：字节字符串，表示的是一个字节串。

例子：
```python
print(b"hello")  # 输出：b'hello'
```

4. `u"..."` ： Unicode 字符串，能够显示比 ASCII 码更多的字符。

例子：
```python
print(u"你好")  # 输出：你好
```