from pyecharts import options as opts
from pyecharts.charts import Map
import pymysql
import pandas as pd
# import datetime
from SoloProject.plague_analyze import JsonResponse
import json


def shuju02():
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="shixun0515",
        charset="utf8"
    )

    cur = con.cursor()
    # 2023年6月2日：下面这句话是当前时间格式化的意思，
    # 因为爬取的网站失效，没有这个时间的数据，只能注释掉
    # curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    # 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
    curdata = "2022-11-08"
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


def sfyqmap02(pm) -> Map:
    sequence = sfdtcha(pm)
    # 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
    # year = datetime.datetime.now().strftime("%Y-%m-%d") + pm
    year = "2022-11-08" + pm
    c = (
        Map(init_opts=opts.InitOpts(width='1000px', height='500px'))
            .add(series_name=year, data_pair=sequence, maptype="china")
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=130, min_=95),
        )
    ).dump_options_with_quotes()
    return JsonResponse(json.loads(c))


if __name__ == "__main__":
    sfyqmap02("现存确诊")
