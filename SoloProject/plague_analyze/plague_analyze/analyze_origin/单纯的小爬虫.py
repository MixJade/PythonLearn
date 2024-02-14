import requests
from lxml import etree
import json
# 导入时间函数
import datetime
import pymysql


def shujutongji():
    print("开始爬取全国疫情数据")
    # 爬取丁香网的国内疫情
    url = "https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0"
    print("在2023-6-2进行测试，这个网站失效了，所以无法爬取数据")
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

    shujuqgtj = (
        curdata,
        qgqz,
        qgljqz,
        qgsw,
        qgzy
    )

    print("当前时间" + curdata)
    print("全国现存确诊人数" + str(qgqz))
    print("全国累计确诊人数" + str(qgljqz))
    print("全国累计死亡人数" + str(qgsw))
    print("全国累计治愈人数" + str(qgzy))
    print(shujuqgtj)
    list03 = [shujuqgtj]
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
        database="play",
        charset="utf8"
    )
    # 创建游标
    cur = con.cursor()
    # 定义sql
    sql = "insert into yqqg0529 " \
          "(时间,现存确诊,累计确诊,累计死亡,累计治愈) " \
          "values(%s,%s,%s,%s,%s)"
    cur.executemany(sql, charu)
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
        database="play",
        charset="utf8"
    )
    cur = con.cursor()
    # 获取当前时间
    curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    # 定义sql查询
    sql = "select * from yqsf0529 where 时间='%s'" % curdata
    # 执行查询
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    print(len(rs))
    return len(rs)


def shengf():
    print("开始爬取各省份的疫情数据")
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


def shujucharu02(charu):
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="play",
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
        database="play",
        charset="utf8"
    )
    cur = con.cursor()
    # 获取当前时间
    curdata = datetime.datetime.now().strftime("%Y-%m-%d")
    # 定义sql查询
    sql = "select * from yqsf0529 where 时间='%s'" % curdata
    # 执行查询
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    con.commit()
    return len(rs)


if __name__ == "__main__":
    shujutongji()
    shengf()
