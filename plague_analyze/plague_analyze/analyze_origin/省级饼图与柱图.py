import json
import os

# 导入时间函数
import pandas as pd
from django.http import JsonResponse
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.charts import Pie


# noinspection  NonAsciiCharacters,PyPep8Naming
def 根据当前时间查省份数据():
    # 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
    当前时间 = "2022-11-08"
    path = os.path.abspath(os.path.join(os.getcwd(), "inputFile", "province0529.csv"))
    df = pd.read_csv(path)
    return df[df['时间'] == 当前时间]


# noinspection  NonAsciiCharacters,PyPep8Naming
def 根据列名画前10名柱状图(pm: str) -> JsonResponse:
    # 运行查询数据，获取结果
    省份数据 = 根据当前时间查省份数据()
    df = 省份数据[["省份名称", "现存确诊", "累计确诊", "治愈人数", "死亡人数"]]
    if pm == "现存确诊":
        # 从大到小排序
        df = df.sort_values(by="现存确诊")
        # 把数据转换成列表,取出名字
        list_key = list(df["省份名称"])[-10:]
        list_val = list(df["现存确诊"])[-10:]
    elif pm == "累计确诊":
        df = df.sort_values(by="累计确诊")
        list_key = list(df["省份名称"])[-10:]
        list_val = list(df["累计确诊"])[-10:]
    elif pm == "治愈人数":
        df = df.sort_values(by="治愈人数")
        list_key = list(df["省份名称"])[-10:]
        list_val = list(df["治愈人数"])[-10:]
    else:
        df = df.sort_values(by="死亡人数")
        list_key = list(df["省份名称"])[-10:]
        list_val = list(df["死亡人数"])[-10:]

    # 存入字典
    d = {"x": list_key, "y": list_val}
    return 用前10省份字典画柱状图(d)


# 画图
# noinspection  NonAsciiCharacters,PyPep8Naming
def 用前10省份字典画柱状图(d: dict[str, list]) -> JsonResponse:
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


# noinspection  NonAsciiCharacters,PyPep8Naming
def 构建饼图需要的数据结构(bm: str) -> tuple[tuple[str, int], tuple[str, int], tuple[str, int]]:
    # 运行查询数据库，获取结果
    省份数据 = 根据当前时间查省份数据()
    # 把listData转换成pandas的数据帧
    df = 省份数据[["省份名称", "现存确诊", "治愈人数", "死亡人数"]]
    df = df.groupby("省份名称")  # 依据名查询
    df = df.get_group(bm)

    # 构建饼图需要的数据结构
    t = (
        ("现存确诊", int(df["现存确诊"].iloc[0])),
        ("治愈人数", int(df["治愈人数"].iloc[0])),
        ("死亡人数", int(df["死亡人数"].iloc[0]))
    )
    return t


# noinspection  NonAsciiCharacters,PyPep8Naming
def 根据省份名画饼状图(bm: str) -> JsonResponse:
    # 构建饼图需要的数据结构
    t = 构建饼图需要的数据结构(bm)
    p = (
        Pie()
        .add("%s的疫情数据分析" % bm, t)
        .set_colors(["red", "yellow", "black"])

    ).dump_options_with_quotes()
    return JsonResponse(json.loads(p))
