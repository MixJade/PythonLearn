# coding=utf-8
# @Time    : 2026/3/18 21:08
# @Software: PyCharm

def decimal_to_little_endian(decimal_num: int):
    """将十进制数转换为4字节小端序格式"""
    # 补全为4字节（8位十六进制，大写）
    full_hex = f"{decimal_num:08X}"
    print(f"  16进制转换：{full_hex}")
    # 拆分字节并按小端序排列
    bytes_list = [full_hex[i:i + 2] for i in range(0, 8, 2)]
    little_endian = " ".join(reversed(bytes_list))
    print(f"  小端序存储结果：{little_endian}\n")
    return little_endian


# 主循环：循环询问，输入0退出
print("=== 十进制转4字节小端序工具 ===")

while True:
    # 获取用户输入
    user_input = input("请输入十进制数（输0退出）：").strip()

    # 处理退出条件
    if user_input == "0":
        print("程序已退出！")
        break

    # 处理非数字输入
    try:
        input_num = int(user_input)
        # 调用转换函数
        decimal_to_little_endian(input_num)
    except ValueError:
        print("❌ 输入错误！请输入有效的十进制整数（如322）\n")
