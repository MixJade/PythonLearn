from  pyecharts import options as opts
from pyecharts.charts import Map
import pymysql
import pandas as pd
import datetime


def shuju02():
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="shixun0515",
        charset="utf8"
    )

    cur = con.cursor()
    curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    # 定义sql查询
    sql = "select * from yqsf0529 where 时间='%s'" % curdata
    # 执行批量插入
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    cur.close()
    return rs


def sfdtcha(pm):
    # 运行查询数据，获取结果
    sfshuju = shuju02()
    df = pd.DataFrame(sfshuju, columns=["id", "time", "sf", "xcqz", "ljqz", "zy", "sw"])
    listx = list(df["sf"])
    if pm == "现存确诊":
        # 把数据转换成列表,取出名字
        listy = list(df["xcqz"])
    elif pm == "累计确诊":
        listy = list(df["ljqz"])
    elif pm == "治愈人数":
        listy = list(df["zy"])
    else:
        listy = list(df["sw"])

    # 存入字典
    dtsj = list(zip(listx, listy))
    return dtsj


def sfyqmap(pm) -> Map:
    sequence = sfdtcha(pm)
    year = datetime.datetime.now().strftime("%Y-%m-%d") + pm
    c = (
        Map(opts.InitOpts(width='1200px', height='600px'))  # opts.InitOpts() 设置初始参数:width=画布宽,height=画布高
        .add(series_name=year, data_pair=sequence, maptype="china")  # 系列名称(显示在中间的名称 )、数据 、地图类型
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=130, min_=95),
        )
    )
    return c


def mapwulai(pm):
    mapwu = sfyqmap(pm)
    mapwu.render(path='地图分析之里.html')


if __name__ == "__main__":
    mapwulai("现存确诊")
