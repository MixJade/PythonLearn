import requests
from lxml import etree
import json
from SoloProject.plague_analyze import JsonResponse
# 导入时间函数
import datetime
import pymysql
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar


def shujutongji():
    # 爬取丁香网的国内疫情
    url = "https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0"
    rs = requests.get(url)
    rs.encoding = "utf-8"
    body = rs.text
    html = etree.HTML(body)
    # 提取国内疫情数据
    list01 = html.xpath("//script[@id='getAreaStat']/text()")
    info = str(list01)
    info = info[29:-13]
    list02 = json.loads(info)
    # 获取当前时间
    curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    qgqz = 0
    qgljqz = 0
    qgsw = 0
    qgzy = 0
    for i in range(len(list02)):
        qgqz = qgqz + list02[i]["currentConfirmedCount"]
        qgljqz = qgljqz + list02[i]["confirmedCount"]
        qgsw = qgsw + list02[i]["deadCount"]
        qgzy = qgzy + list02[i]["curedCount"]

    shujuqgtj =(
        curdata,
        qgqz,
        qgljqz,
        qgsw,
        qgzy
    )

    print("当前时间"+curdata)
    print("全国现存确诊人数"+str(qgqz))
    print("全国累计确诊人数"+str(qgljqz))
    print("全国累计死亡人数"+str(qgsw))
    print("全国累计治愈人数"+str(qgzy))
    print(shujuqgtj)
    list03 = [shujuqgtj, shujuqgtj]
    # 判断数据库是否有今天的数据
    rs = valdata()
    if rs > 0:
        print("今日数据已经爬取")
    else:
        shujucharu(list03)


def shujucharu(charu):
    con = pymysql.Connect(
                host="localhost",
                user="root",
                passwd="root",
                database="shixun0515",
                charset="utf8"
                )
    # 创建游标
    cur = con.cursor()
    # 定义sql
    sql = "insert into yqqg0529 " \
          "(时间,现存确诊,累计确诊,累计死亡,累计治愈) " \
          "values(%s,%s,%s,%s,%s)"
    cur.executemany(sql,charu)
    # 获取结果集
    rs = cur.rowcount
    # 提交
    con.commit()
    if rs > 0:
        print("插入成功")
    else:
        print("插入失败")


def valdata():
    # 创建数据库连接
    con = pymysql.Connect(
                host="localhost",
                user="root",
                passwd="root",
                database="shixun0515",
                charset="utf8"
                )
    cur = con.cursor()
    # 获取当前时间
    # curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    # 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
    curdata = "2022-11-08"
    # 定义sql查询
    sql = "select * from yqsf0529 where 时间='%s'" % curdata
    # 执行查询
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    print(len(rs))
    return len(rs)


def shuju01():
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="shixun0515",
        charset="utf8"
    )

    cur = con.cursor()
    # 定义sql查询
    sql = "select * from yqqg0529"
    # 执行批量插入
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    cur.close()
    return rs


def qgyqcha(km):
    # 运行查询数据，获取结果
    sfshuju = shuju01()
    df = pd.DataFrame(sfshuju, columns=["time", "xcqz", "ljqz", "zy", "sw"])
    listx = list(df["time"])
    if km == "现存确诊":
        # 从大到小排序
        df = df.sort_values(by="xcqz")
        # 把数据转换成列表,取出名字
        listy = list(df["xcqz"])
    elif km == "累计确诊":
        df = df.sort_values(by="ljqz")
        listy = list(df["ljqz"])
    elif km == "治愈人数":
        df = df.sort_values(by="zy")
        listy = list(df["zy"])
    else:
        df = df.sort_values(by="sw")
        listy = list(df["sw"])

    # 存入字典
    d = {"x": listx, "y": listy}
    return testqgyq05(d)


def testqgyq05(d):

    b = (
        Bar()
        .add_xaxis(d["x"])
        .add_yaxis("全国疫情时间排名", d["y"])
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                # 设置x轴刻度不显示
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                # 设置y轴字体颜色
                axislabel_opts=opts.LabelOpts(color="white"),
                # 设置 y轴刻度不显示
                axistick_opts=opts.AxisTickOpts(is_show=False)
            ),
            # 不显示图例组件的汉字
            legend_opts=opts.LegendOpts(is_show=True),
        )
        .set_series_opts(
            # 设置数值字体靠靠右边显示
            label_opts=opts.LabelOpts(position="right"),
        )
        # 翻转
        # .reversal_axis()
        .set_colors(["yellow"])
        ).dump_options_with_quotes()
    # 返回json数据
    return JsonResponse(json.loads(b))


def qgbingcshu(jm):
    # 运行查询数据库，获取结果
    sfshuju02 = shuju01()
    # 把listData转换成pandas的数据帧
    df = pd.DataFrame(sfshuju02, columns=["time", "xcqz", "ljqz", "zy", "sw"])
    df = df.groupby("time")  # 依据名查询
    df = df.get_group(jm)

    print(df)
    # 构建饼图需要的数据结构
    t = (
        ("现存确诊", int(df["xcqz"])),
        ("治愈人数", int(df["zy"])),
        ("死亡人数", int(df["sw"]))
    )
    print(t)
    return t


def qgtestbing(jm):
    # 构建饼图需要的数据结构
    t = qgbingcshu(jm)
    p = (
        Pie()
        .add("%s的疫情数据分析" % jm, t)
        .set_colors(["red", "yellow", "black"])

    ).dump_options_with_quotes()
    return JsonResponse(json.loads(p))


if __name__ == "__main__":
    shujutongji()
