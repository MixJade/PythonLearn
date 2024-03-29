# 导入时间函数
import json
import os

import pandas as pd
from django.http import JsonResponse
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie


# noinspection  NonAsciiCharacters,PyPep8Naming
def 查询国级数据():
    path = os.path.abspath(os.path.join(os.getcwd(), "inputFile", "nation0529.csv"))
    return pd.read_csv(path)


# noinspection  NonAsciiCharacters,PyPep8Naming
def 根据列名绘制全国疫情时间柱状图(km: str) -> JsonResponse:
    # 运行查询数据，获取结果
    国级数据 = 查询国级数据()
    df = 国级数据[["时间", "现存确诊", "累计确诊", "累计治愈", "累计死亡"]]
    list_key = list(df["时间"])
    if km == "现存确诊":
        # 从大到小排序
        df = df.sort_values(by="现存确诊")
        # 把数据转换成列表,取出名字
        list_val = list(df["现存确诊"])
    elif km == "累计确诊":
        df = df.sort_values(by="累计确诊")
        list_val = list(df["累计确诊"])
    elif km == "累计治愈":
        df = df.sort_values(by="累计治愈")
        list_val = list(df["累计治愈"])
    else:
        df = df.sort_values(by="累计死亡")
        list_val = list(df["累计死亡"])

    # 存入字典
    d = {"x": list_key, "y": list_val}
    return 绘制全国疫情时间柱状图(d)


# noinspection  NonAsciiCharacters,PyPep8Naming
def 绘制全国疫情时间柱状图(d: dict[str, list]) -> JsonResponse:
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


# noinspection  NonAsciiCharacters,PyPep8Naming
def 返回某日全国疫情数据(jm: str) -> tuple[tuple[str, int], tuple[str, int], tuple[str, int]]:
    # 运行查询数据库，获取结果
    国级数据2 = 查询国级数据()
    # 把listData转换成pandas的数据帧
    df = 国级数据2[["时间", "现存确诊", "累计治愈", "累计死亡"]]
    df = df.groupby("时间")  # 依据名查询
    df = df.get_group(jm)
    # 构建饼图需要的数据结构
    return (
        ("现存确诊", int(df["现存确诊"].iloc[0])),
        ("累计治愈", int(df["累计治愈"].iloc[0])),
        ("累计死亡", int(df["累计死亡"].iloc[0]))
    )


# noinspection  NonAsciiCharacters,PyPep8Naming
def 根据日期绘制全国疫情饼状图(jm):
    # 构建饼图需要的数据结构
    t = 返回某日全国疫情数据(jm)
    p = (
        Pie()
        .add("%s的疫情数据分析" % jm, t)
        .set_colors(["red", "yellow", "black"])

    ).dump_options_with_quotes()
    return JsonResponse(json.loads(p))
