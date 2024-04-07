import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map


def province_data(pm: str) -> list[tuple[str, str]]:
    # 运行查询数据，获取结果
    province_1108 = pd.read_csv("../../A1输入数据/province1108.csv")
    df = province_1108[["时间", "省份名称", "现存确诊", "累计确诊", "治愈人数", "死亡人数"]]
    list_key = list(df["省份名称"])
    if pm == "现存确诊":
        # 把数据转换成列表,取出名字
        list_val = list(df["现存确诊"])
    elif pm == "累计确诊":
        list_val = list(df["累计确诊"])
    elif pm == "治愈人数":
        list_val = list(df["治愈人数"])
    else:
        list_val = list(df["死亡人数"])

    # 存入字典
    return list(zip(list_key, list_val))


def get_map_data(pm) -> Map:
    sequence = province_data(pm)
    year = "2022-11-08" + pm
    c = (
        Map(opts.InitOpts(width='1200px', height='600px'))  # opts.InitOpts() 设置初始参数:width=画布宽,height=画布高
        .add(series_name=year, data_pair=sequence, maptype="china")  # 系列名称(显示在中间的名称 )、数据 、地图类型
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=130, min_=95),
        )
    )
    return c


def paint_map(pm):
    map_data = get_map_data(pm)
    map_data.render(path='../../A2兼收并蓄/地图分析之里.html')


if __name__ == "__main__":
    paint_map("现存确诊")
