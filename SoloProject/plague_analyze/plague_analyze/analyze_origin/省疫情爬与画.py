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


def shengf():
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
    shengf02 = []
    for i in range(len(list02)):
        print("省份名称：", list02[i]["provinceShortName"])
        print("现存确诊：", list02[i]["currentConfirmedCount"])
        print("累计确诊：", list02[i]["confirmedCount"])
        print("治愈人数：", list02[i]["curedCount"])
        print("死亡人数：", list02[i]["deadCount"])
        shengf01 = (
            i,
            curdata,
            list02[i]["provinceShortName"],
            list02[i]["currentConfirmedCount"],
            list02[i]["confirmedCount"],
            list02[i]["curedCount"],
            list02[i]["deadCount"]
        )
        shengf02.append(shengf01)
    print(len(list02))
    print(shengf02)

    rs = valdata02()
    if rs > 0:
        print("今日数据已经爬取")
    else:
        shujucharu02(shengf02)


def shuju02():
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="shixun0515",
        charset="utf8"
    )

    cur = con.cursor()
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


def shujucharu02(charu):
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
    sql = "insert into yqsf0529 " \
          "(序列,时间,省份名称,现存确诊,累计确诊,治愈人数,死亡人数) " \
          "values(%s,%s,%s,%s,%s,%s,%s)"
    cur.executemany(sql, charu)
    # 获取结果集
    rs = cur.rowcount
    # 提交
    con.commit()
    if rs > 0:
        print("插入成功")
    else:
        print("插入失败")


def valdata02():
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
    con.commit()
    return len(rs)


def sfyqcha(pm):
    # 运行查询数据，获取结果
    sfshuju = shuju02()
    df = pd.DataFrame(sfshuju, columns=["id", "time", "sf", "xcqz", "ljqz", "zy", "sw"])
    if pm == "现存确诊":
        # 从大到小排序
        df = df.sort_values(by="xcqz")
        # 把数据转换成列表,取出名字
        listx = list(df["sf"])[-10:]
        listy = list(df["xcqz"])[-10:]
    elif pm == "累计确诊":
        df = df.sort_values(by="ljqz")
        listx = list(df["sf"])[-10:]
        listy = list(df["ljqz"])[-10:]
    elif pm == "治愈人数":
        df = df.sort_values(by="zy")
        listx = list(df["sf"])[-10:]
        listy = list(df["zy"])[-10:]
    else:
        df = df.sort_values(by="sw")
        listx = list(df["sf"])[-10:]
        listy = list(df["sw"])[-10:]

    # 存入字典
    d = {"x": listx, "y": listy}
    return print_picture(d)


# 画图
def print_picture(d):

    b = (
        Bar()
        .add_xaxis(d["x"])
        .add_yaxis("省份疫情前10排名", d["y"])
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                # 设置x轴字体不显示
                axislabel_opts=opts.LabelOpts(is_show=False),
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
        .reversal_axis()
        .set_colors(["orange"])
        ).dump_options_with_quotes()
    # 返回json数据
    return JsonResponse(json.loads(b))


def sfbingcshu(bm):
    # 运行查询数据库，获取结果
    sfshuju02 = shuju02()
    # 把listData转换成pandas的数据帧
    df = pd.DataFrame(sfshuju02, columns=["id", "time", "sf", "xcqz", "ljqz", "zy", "sw"])
    df = df.groupby("sf")  # 依据名查询
    df = df.get_group(bm)

    print(df)
    # 构建饼图需要的数据结构
    t = (
        ("现存确诊", int(df["xcqz"])),
        ("治愈人数", int(df["zy"])),
        ("死亡人数", int(df["sw"]))
    )
    print(t)
    return t


def testbing(bm):
    # 构建饼图需要的数据结构
    t = sfbingcshu(bm)
    p = (
        Pie()
        .add("%s的疫情数据分析" % bm, t)
        .set_colors(["red", "yellow", "black"])

    ).dump_options_with_quotes()
    return JsonResponse(json.loads(p))


if __name__ == "__main__":
    shengf()

