# Python除法输出分数

Python中，可以使用`fractions`模块实现分数的输出，这是一个内置的模块，可以直接导入使用。

以下是一个例子：

```python
from fractions import Fraction

# 创建两个整数
a = 3
b = 7

# 使用 Fraction 创建分数
result = Fraction(a, b)

# 打印出分数形式的结果
print(result)
```

这个脚本的输出会是`3/7`，这就是`fractions`模块的简单使用方式。