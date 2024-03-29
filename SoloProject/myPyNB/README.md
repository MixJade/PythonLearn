# README

* 这里是Jupyter的文件夹，推荐用anaconda3所附带的Jupyter打开
* 更改Jupyter的文件夹路径，不然用Jupyter打不开这个文件夹
* 我电脑上Jupyter的配置文件路径：`"C:\Users\{QQ号}\.jupyter\jupyter_notebook_config.py"`
* 进去搜索:`pyJade`，那个绝对路径就是

## 其它电脑的路径

打开文件：

```text
C:\#{你电脑上的用户文件夹}\.jupyter\jupyter_notebook_config.py
```

进去搜索：

```python
## The directory to use for notebooks and kernels.
#  Default: ''
c.NotebookApp.notebook_dir = '/'  # 这里是后面自己改的路径
```

然后修改：

```python
c.NotebookApp.notebook_dir = '#{你想将Jupyter文件存放的位置}'
```

## 选择excel特定行之后的所有行

> 用于裁剪数据集，防止文件过大

1. 选中“特定行”，这个可以将右上角的【A1】改成【A1001】快速跳转。
2. ctrl+shift+下箭头,将会直接*选择*到最后一行。
