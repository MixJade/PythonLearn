# coding=utf-8
# @Time    : 2024/2/4 16:08
# @Software: PyCharm
import random

import pandas as pd

"""大数据作业三数据分析所用的csv是这里生成的
"""
Id = list(range(10001, 10101))
usrNo = [random.choice([1, 2, 3, 4, 5, 6]) for _ in range(100)]
login_locations = [random.choice(["东莞", "赤峰", "银川", "辽阳", "南平", "宜昌", "温州", "深圳"]) for _ in range(100)]
usrId = usrNo
usrNm = ["张三" if user_no == 1 else
         "李四" if user_no == 2 else
         "王五" if user_no == 3 else
         "赵六" if user_no == 4 else
         "田七" if user_no == 5 else
         "老八" if user_no == 6 else
         "无名" for user_no in usrNo]
login_dates = [random.choice(pd.date_range("2014/2/20", "2015/2/20")) for _ in range(100)]
login_type = [random.choice(["Iphone", "XiaoMi", "HuaWei", "Oppo"]) for _ in range(100)]
registration_dates = ["2014/1/21" if user_no == 1 else "2014/2/22" if user_no == 2 else "2014/2/26" for user_no in
                      usrNo]
export_dates = ["2015/2/20"] * 20 + ["2015/2/22"] * 20 + ["2015/3/1"] * 60
login_status = ["1"] * 95 + ["0"] * 5
edu_acc_status = ["1"] * 100

data = list(
    zip(Id, usrNo, login_locations, usrId, usrNm, login_dates, login_type, registration_dates, export_dates,
        login_status,
        edu_acc_status))

df = pd.DataFrame(data)
df.columns = ["Idx", "usrNo", "登录地", "usrId", "姓名", "登录日期", "登录机型", "注册日期", "导出日期", "是否正常登录",
              "是否是教育账号"]

df.to_csv("../../outputFile/train_data.csv", index=False)
