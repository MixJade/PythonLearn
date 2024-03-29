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