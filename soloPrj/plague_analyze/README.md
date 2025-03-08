# 爬取疫情数据并进行可视化分析

* 使用django框架
* 2023年6月2日更新：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据 
* 目前只在`plague_analyze/analyze_origin/地图之画.py`中，替换掉当前数据
* 2024年3月30日更新：去掉操作MySQL，改用csv，且部分函数名改为中文

## 2023年6月2日替换的代码

替换前：
```text
curdata = datetime.datetime.now().strftime("%Y-%m-%d")
```
替换后：
```text
# curdata = datetime.datetime.now().strftime("%Y-%m-%d")
# 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
curdata = "2022-11-08"
```

## 设置setting.py

> * 先下载django,
> * 然后`django-admin startproject Hello_WORLD`来获取`setting.py`文件
> * 接下来把`Hello_WORLD`文件删了就行

因为`setting.py`文件里面的密钥会引起github给我发邮件 ，所以教如何设置`setting.py`文件。

1. 第14行，添加`import os`
2. 在第77-82行，屏蔽(注释)掉默认数据库
3. 在119行，加入静态页面的配置

```
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"), )
```

## 创建django项目

> 如果你连django项目都没有创建的话

先在终端下载，并创建

```
pip install django
django-admin help
django-admin startproject Hello_WORLD
```

## 启动django项目

```python manage.py runserver localhost:8000```
然后在浏览器打开`汇总网页.html`

## 前端所依赖的JS库

> 通过cdn的方式从网上获取，这里只列出网上的

|名称|版本|描述|
|:---|:---|:---|
|jquery|1.11.3|这是老师用的版本，看起来非常古老|
|echarts|5.4.2|其实版本未知，这是我现在最新的，但能用|