import requests
from lxml import etree
import json
# 导入时间函数
import datetime
import pymysql


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
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 时间
    shengf02 = []
    for i in range(len(list02)):
        print("省份名称：", list02[i]["provinceShortName"])
        print("现存确诊：", list02[i]["currentConfirmedCount"])
        print("累计确诊：", list02[i]["confirmedCount"])
        print("治愈人数：", list02[i]["curedCount"])
        print("死亡人数：", list02[i]["deadCount"])
        shengf01 = (
            i,
            cur_date,
            list02[i]["provinceShortName"],
            list02[i]["currentConfirmedCount"],
            list02[i]["confirmedCount"],
            list02[i]["curedCount"],
            list02[i]["deadCount"]
        )
        shengf02.append(shengf01)
    print(len(list02))
    print(shengf02)

    rs = val_data02()
    if rs > 0:
        print("今日数据已经爬取")
    else:
        shujucharu02(shengf02)


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


def val_data02():
    # 创建数据库连接
    con = pymysql.Connect(
        host="localhost",
        user="root",
        passwd="root",
        database="shixun0515",
        charset="utf8"
    )
    # 创建游标
    cur = con.cursor()
    # 获取当前时间
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")
    # 定义sql查询
    sql = "select * from yqsf0529 where 时间='%s'" % cur_date
    # 执行查询
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    print(len(rs))
    return len(rs)


if __name__ == "__main__":
    shengf()
