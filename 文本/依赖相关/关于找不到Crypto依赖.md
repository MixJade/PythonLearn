# 关于找不到Crypto依赖

> 2024年2月13日10:16:29(解决方案只限windows)

python 在 Windows下使用AES时要安装的是pycryptodome 模块

> pip install pycryptodome

python 在 Linux下使用AES时要安装的是pycrypto模块

> pip install pycrypto

## 一、问题描述

```python
from Crypto.Cipher import AES
# 出现报错：未解析的引用 'Crypto'
```

## 二、解决办法

```bash
pip uninstall crypto
pip uninstall pycryptodome
pip install pycryptodome
```

## 三、问题原因
首先你要知道 导入的这个模块中的AES是在pycryptodome这个库里面的,

所以 crypto这个库对你来说是没用的。

而如果你装了crypto 这个库, 这两个库会安装到同一个文件夹, 然后本应该 Crypto 这个大写的文件夹变成小写 crypto(因为windows本身不区分大小写),

 这样就会导致找不到这个模块, 两个库的名字发生冲突。

另外看到很多文章解决办法是: 改文件夹名字, 将小写c改为大写C, 

这样虽然也能解决, 但不是问题的根本原因,

 根本原因就是 windows 不区分大小写, 所以卸载无用的库是最好的解决办法!