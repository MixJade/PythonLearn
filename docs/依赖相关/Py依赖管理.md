# Py依赖管理

可以使用pip来管理项目的依赖项，将依赖项信息写入一个名为requirements.txt的文件中。

在requirements.txt文件中，你可以指定每一个依赖项的准确版本。例如：

```
requests==2.18.4
Django==2.0.7
numpy==1.14.5
```

然后，只要用pip install -r requirements.txt命令，pip就会自动安装指定版本的依赖项。

对于更复杂的项目，Python还有其他的工具，比如Pipenv和Poetry，它们可以更好地管理项目的依赖项和虚拟环境，这能够帮助解决不同项目之间由于依赖项版本不同而导致的冲突问题。

## 生成requirements

在终端输入：(通过本地安装的依赖，会显示安装时的文件路径)

```bash
pip freeze > requirements.txt
```

## 卸载依赖

要使用 pip 卸载某个依赖包，可以使用 `pip uninstall` 命令，具体格式如下：

```bash
pip uninstall 包名
```

## 查看依赖版本

执行后会显示该包的详细信息，其中 `Version` 字段就是版本号

```bash
pip show 包名
```

* 以上命令样例：`pip show requests`
* 可以顺便看包的具体位置