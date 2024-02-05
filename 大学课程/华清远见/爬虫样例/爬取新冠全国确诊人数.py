import requests
from lxml import etree
import json
# 导入时间函数
import datetime
import pymysql


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
    cur_date = datetime.datetime.now().strftime("%Y-%m-%d")  # 时间
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
        cur_date,
        qgqz,
        qgljqz,
        qgsw,
        qgzy
    )

    print("当前时间" + cur_date)
    print("全国现存确诊人数" + str(qgqz))
    print("全国累计确诊人数" + str(qgljqz))
    print("全国累计死亡人数" + str(qgsw))
    print("全国累计治愈人数" + str(qgzy))
    print(shujuqgtj)
    list03 = [shujuqgtj]
    # 判断数据库是否有今天的数据
    rs = val_data()
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
    cur.executemany(sql, charu)
    # 获取结果集
    rs = cur.rowcount
    # 提交
    con.commit()
    if rs > 0:
        print("插入成功")
    else:
        print("插入失败")


def val_data():
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
    sql = "select * from yqqg0529 where 时间='%s'" % cur_date
    # 执行查询
    cur.execute(sql)
    # 获取结果集
    rs = cur.fetchall()
    print(len(rs))
    return len(rs)


if __name__ == "__main__":
    shujutongji()
