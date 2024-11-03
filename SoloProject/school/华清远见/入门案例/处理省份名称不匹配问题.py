# coding=utf-8
# @Time    : 2024/4/7 16:21
# @Software: PyCharm
import pandas as pd

province_0529 = pd.read_csv("../../A1输入数据/province1108.csv")
df = province_0529[["时间", "省份名称", "现存确诊", "累计确诊", "治愈人数", "死亡人数"]]

df.loc[df["省份名称"] == "新疆", "省份名称"] = "新疆维吾尔自治区"
df.loc[df["省份名称"] == "广西", "省份名称"] = "广西壮族自治区"
df.loc[df["省份名称"] == "宁夏", "省份名称"] = "宁夏回族自治区"
df.loc[df["省份名称"].isin(["内蒙古", "西藏"]), "省份名称"] = df["省份名称"] + "自治区"
df.loc[df["省份名称"].isin(["北京", "天津", "重庆", "上海"]), "省份名称"] = df["省份名称"] + "市"
df.loc[df["省份名称"].isin(["香港", "澳门"]), "省份名称"] = df["省份名称"] + "特别行政区"
df.loc[~df["省份名称"].str.contains("自治区|市|特别行政区|省"), "省份名称"] = df["省份名称"] + "省"

# print(df)
df.to_csv("../../A1输入数据/province1108.csv", index=False)
