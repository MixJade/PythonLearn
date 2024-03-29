import json
import os

import pandas as pd
from django.http import JsonResponse
from pyecharts import options as opts
from pyecharts.charts import Map


# noinspection  NonAsciiCharacters,PyPep8Naming
def 用列名查省份数据(pm: str) -> list[tuple[str, str]]:
    # 运行查询数据，获取结果
    path = os.path.abspath(os.path.join(os.getcwd(), "inputFile", "province0529.csv"))
    各省数据 = pd.read_csv(path)
    df = 各省数据[["时间", "省份名称", "现存确诊", "累计确诊", "治愈人数", "死亡人数"]]
    当前时间 = "2022-11-08"
    df = df[df['时间'] == 当前时间]

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


# noinspection  NonAsciiCharacters,PyPep8Naming,SpellCheckingInspection
def 返回各省地图数据(pm: str) -> JsonResponse:
    sequence = 用列名查省份数据(pm)
    # 2023年6月2日：因为爬取的网站失效了，数据无法获取，只能用数据库最后的数据
    # year = datetime.datetime.now().strftime("%Y-%m-%d") + pm
    year = "2022-11-08" + pm
    c = (
        Map(init_opts=opts.InitOpts(width='1000px', height='500px'))
        .add(series_name=year, data_pair=sequence, maptype="china")
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=130, min_=95),
        )
    ).dump_options_with_quotes()
    return JsonResponse(json.loads(c))
