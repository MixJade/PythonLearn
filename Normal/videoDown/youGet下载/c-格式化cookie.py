# coding=utf-8
# @Time    : 2025/2/22 10:18
# @Software: PyCharm
import time


def format_cookies(cookie_string, domain=".bilibili.com", path="/", secure="FALSE"):
    """
    将 Cookie 字符串格式化为 Netscape HTTP Cookie File 格式

    :param cookie_string: 原始 Cookie 字符串
    :param domain: 域名
    :param path: 路径
    :param secure: 安全标志
    :return: 格式化后的 Cookie 文本
    """
    # 分割 Cookie 字符串
    cookies = cookie_string.split("; ")
    # 获取当前时间戳
    current_time = int(time.time())
    # 默认过期时间，设置为一年后
    default_expires = current_time + 365 * 24 * 60 * 60

    # 初始化格式化后的文本
    formatted_text = "# Netscape HTTP Cookie File\n"
    formatted_text += "# https://curl.haxx.se/rfc/cookie_spec.html\n"
    formatted_text += "# This is a generated file!  Do not edit.\n\n"

    for cookie in cookies:
        try:
            name, value = cookie.split("=", 1)
            # 检查是否有明确的过期时间
            if name == "bili_ticket_expires":
                expires = int(value)
            else:
                expires = default_expires
            # 格式化每一行
            line = f"{domain}\tTRUE\t{path}\t{secure}\t{expires}\t{name}\t{value}\n"
            formatted_text += line
        except ValueError:
            print(f"无法解析 Cookie: {cookie}")

    return formatted_text


def main():
    try:
        # 以读取模式打开文件
        with open("a-原初cookie.txt", "r", encoding="utf-8") as ori_file:
            # 读取第一行
            cookie_string = ori_file.readline().strip()
            if not cookie_string:
                print("原初cookie文件为空。")
                return
            # 格式化 Cookie
            formatted_cookies = format_cookies(cookie_string)
            # 写入格式化后的 Cookie 到文件
            with open("b-cookies.txt", "w", encoding="utf-8") as file:
                file.write(formatted_cookies)
            print("Cookie 文件已生成：b-cookies.txt")
    except FileNotFoundError:
        print("原初cookie文件未找到。")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()
