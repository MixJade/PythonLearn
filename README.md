# python学习笔记
> 关于机器学习，Python的各种文件操作，以及爬虫，django

|  开发工具   |    开发环境    |
|:-------:|:----------:|
| pyCharm | python3.10 |

1. 里面大部分代码在学习的时候，是基于python3.10
2. 大四说换成了anaconda3自带的python3.9，但有些兼容问题，比如`pygame库`安装不了
3. (2024-3-29)现在毕业后换成了3.10

---

## 目录结构

```text
├─docs
│  ├─代码语法
│  ├─依赖相关
│  └─闲杂文等
├─myPyNB【Jupyter目录，学习大数据分析时的笔记】
├─Normal
│  ├─dealFile【文件处理】
│  ├─dealCreep【网络爬虫】
│  ├─inputFile【代码运行时输入的文件】
│  ├─outputFile【代码运行时输出的文件】
│  ├─tests【测试代码语法】
│  ├─testSolve【测试算法】
│  ├─toys【玩具代码】
│  └─utils【通过cmd调用的一些工具脚本】
ownWork
└─soloPrj
    ├─autoClick【自动点击框架、Selenium初步使用】
    ├─plague_analyze【实训项目，爬取疫情数据并可视化展示】
    └─school
        ├─A1输入数据【用于输入的文件】
        ├─A2兼收并蓄【输出的数据或者生成的文件都放在这里】
        ├─A3代码废案【花费了精力，但没有用的代码，以txt形式保存】
        ├─华清远见
        │  ├─入门案例【代码入门学习】
        │  └─爬虫样例【小爬虫，现在爬取的网站结构变了，所以全失效了】
        ├─大数据分析【跟上面那个Jupyter的文件夹配套的】
        ├─数学建模【重置大二时的建模论文】
        ├─数据分析与机器学习【关于机器学习的笔记，主要是分类西瓜】
        ├─深度学习 【包括了CNN、RNN、BP网络】
        └─软件与实践【大二时初次学习python的笔记】
            ├─小鸟管道
            └─编程入门
```



## plague_analyze文件夹

>是基于django的项目，爬取国内疫情进行可视化分析

1. 下面有文件夹:**项目启动**，里面有**爬虫脚本.bat**，以及**项目启动.bat**
2. 注意**项目启动.bat**里面，的`call`后面的路径是anaconda3的`\Scripts\activate.bat`文件，以及anaconda3自身的文件夹。
3. 如果你已经配置好了python的环境变量，可以删去`call`及它后面的路径，不然建议更改为自己的python路径
4. 先点击爬虫脚本进行数据的爬取，再点击项目启动的脚本 
 ~~不然数据的日期对不上会导致空网页~~
5. 里面的sql脚本单纯为了规范数据库表的表头与数据格式

---

## 小鸟管道文件夹

> 是基于python3.10的pygame包进行开发， 

后面因为改为python3.9，一直安装不了pygame包，就一直放在里面。
如果要玩游戏，记得用3.10

---

## git五连

```bash
git init
git remote add origin git@github.com:MixJade/PythonLearn.git
git add .
git commit -m "first commit"
git branch -M main
git push -u origin main
```