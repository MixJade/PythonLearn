from SoloProject.plague_analyze import sfyqcha
from SoloProject.plague_analyze import testbing
from SoloProject.plague_analyze import qgyqcha
from SoloProject.plague_analyze import qgtestbing
from SoloProject.plague_analyze import sfyqmap02


def qian01(request):
    print("========qian01==========")
    bm = request.GET.get("bm")
    print("bm=", bm)
    return testbing(bm)


# 接收前端发送的参数
def qian02(request):
    print("========qian02==========")
    pm = request.GET.get("pm")
    print("pm=", pm)
    return sfyqcha(pm)


def qian03(request):
    print("========qian03==========")
    km = request.GET.get("km")
    print("km=", km)
    return qgyqcha(km)


def qian04(request):
    print("========qian04==========")
    jm = request.GET.get("jm")
    print("jm=", jm)
    return qgtestbing(jm)


def qian05(request):
    print("========qian05==========")
    lm = request.GET.get("lm")
    print("lm=", lm)
    return sfyqmap02(lm)
