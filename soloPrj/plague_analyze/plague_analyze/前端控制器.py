from plague_analyze.analyze_origin.国级饼图与柱图 import 根据日期绘制全国疫情饼状图, 根据列名绘制全国疫情时间柱状图
from plague_analyze.analyze_origin.绘制全国各省地图 import 返回各省地图数据
from plague_analyze.analyze_origin.省级饼图与柱图 import 根据列名画前10名柱状图, 根据省份名画饼状图


def qian01(request):
    print("========qian01==========")
    bm = request.GET.get("bm")
    print("bm=", bm)
    return 根据省份名画饼状图(bm)


# 接收前端发送的参数
def qian02(request):
    print("========qian02==========")
    pm = request.GET.get("pm")
    print("pm=", pm)
    return 根据列名画前10名柱状图(pm)


def qian03(request):
    print("========qian03==========")
    km = request.GET.get("km")
    print("km=", km)
    return 根据列名绘制全国疫情时间柱状图(km)


def qian04(request):
    print("========qian04==========")
    jm = request.GET.get("jm")
    print("jm=", jm)
    return 根据日期绘制全国疫情饼状图(jm)


def qian05(request):
    print("========qian05==========")
    lm = request.GET.get("lm")
    print("lm=", lm)
    return 返回各省地图数据(lm)
