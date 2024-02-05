import pymysql


def connect_mysql():
    """连接数据库，查询，插入"""
    connection = pymysql.connect(host="localhost", user="root", passwd="root", database="shixun0515")
    # 下面是py与mysql的通行车辆(游标)
    curcat = connection.cursor()
    sq1 = "select * from students"
    curcat.execute(sq1)
    data01 = curcat.fetchall()
    print(data01)
    print(curcat.fetchall())

    # 第二个操作
    print("第二次操作:")
    data02 = [['没头脑', 60, 60, 1.57, 300], ['不高兴', 60, 70, 1.66, 200]]
    sq2 = "INSERT INTO students(studentName,englishGrade,mathGrade,height,money) VALUES(%s,%s,%s,%s,%s);"
    curcat.executemany(sq2, data02)
    # 查询数据
    curcat.execute(sq1)
    data03 = curcat.fetchall()
    print(data03)
    # 关闭游标和连接
    curcat.close()
    connection.close()


if __name__ == '__main__':
    connect_mysql()
