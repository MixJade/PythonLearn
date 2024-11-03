import configparser

import pymysql


def get_connection():
    """从配置文件读取数据库链接
    """
    config = configparser.ConfigParser()
    config.read('mysql.ini')
    return pymysql.connect(
        host=config['mysql']['host'],
        user=config['mysql']['user'],
        passwd=config['mysql']['password'],
        database=config['mysql']['database'])


def connect_mysql():
    """连接数据库，查询，插入"""
    connection = get_connection()
    # 下面是py与mysql的通行车辆(游标)
    cur_cat = connection.cursor()
    sq1 = "select * from students"
    cur_cat.execute(sq1)
    data01 = cur_cat.fetchall()
    print(data01)
    print(cur_cat.fetchall())

    # 第二个操作
    print("第二次操作:")
    data02 = [['没头脑', 60, 60, 1.57, 300], ['不高兴', 60, 70, 1.66, 200]]
    # 并不会真的插进去，
    # 因为connect的autocommit默认为False，需要调用commit才能改数据库
    sq2 = "INSERT INTO students(studentName,englishGrade,mathGrade,height,money) VALUES(%s,%s,%s,%s,%s);"
    cur_cat.executemany(sq2, data02)
    # 查询数据
    cur_cat.execute(sq1)
    data03 = cur_cat.fetchall()
    print(data03)
    # 提交更改(不提交等于没有改数据库)
    # connection.commit()
    # 关闭游标和连接
    cur_cat.close()
    connection.close()


if __name__ == '__main__':
    connect_mysql()
