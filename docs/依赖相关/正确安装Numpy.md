# 正确安装Numpy

## 一、背景

我之前安装numpy是通过`pip install numpy`来安装的，但安装之后有如下两个问题。

1. 只安装了numpy时，启动有numpy的文件是没有问题。但如果又安装了`matplotlib`(一个画统计图的库)，再启动之前有numpy文件会提示“numpy文件重复导入"(The NumPy module was reloaded)

   ```text
   为什么安装完matplotlib 后，再运行带有numpy库的Py文件会报The NumPy module was reloaded的错，在安装matplotlib 之前没有这种情况
   ```

2. 在安装完matplotlib后，启动带有matplotlib库的py文件会报错：“importError: DLLload failed:找不到指定的模块”

## 二、原因

是numpy版本的问题，直接pip的numpy版本会少DLL。需要下载有mkl的numpy

## 三、解决

去专门的镜像网站：[Python镜像站](https://www.lfd.uci.edu/~gohlke/pythonlibs/)下载带有mkl的numpy，这个在网站的开篇介绍就有。

[numpy下载](https://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy)

我下载的版本是：`"numpy-1.22.4+mkl-cp310-cp310-win_amd64.whl"`

下载速度很慢，建议去找别人的百度网盘资源。

下载完成后，打开python终端，输入以下命令：(install后面是我刚下载的whl文件地址)

```bash
pip install "C:\MyHide\py\whl\numpy-1.22.4+mkl-cp310-cp310-win_amd64.whl"
```