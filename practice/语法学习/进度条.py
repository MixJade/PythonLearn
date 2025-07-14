# coding=utf-8
# @Time    : 2025/7/14 20:46
# @Software: PyCharm
import time

# 进度条的开始计时
start = time.perf_counter()


def progress_bar(it, total):
    # 计算完成百分比
    percent = 100 * (it / float(total))
    # 计算进度条的时间
    do_time = time.perf_counter() - start
    # 构建进度条字符串
    finsh = "█" * i
    need_do = "-" * (total - it)
    # r回到行首，以做到刷新打印的效果
    print(f"\r{percent:^3.0f}%[{finsh}->{need_do}]{do_time:.2f}s", end="")
    # 当进度完成时，打印换行符
    if it == total:
        print()


# 示例用法
t = 100
for i in range(t + 1):
    progress_bar(i, t)
    time.sleep(0.05)  # 模拟工作
