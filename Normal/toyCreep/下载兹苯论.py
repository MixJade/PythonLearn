# coding=utf-8
# @Time    : 2025/2/18 20:21
# @Software: PyCharm
import requests
import chardet
import os

ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}


def down_chapter(url, out_file):
    """下载章节
    """
    # 请求 content
    response = requests.get(f"https://www.marxists.org/chinese/{url}", headers=ua)
    # 检测网页内容的编码
    encoding = chardet.detect(response.content)['encoding']
    html_str = response.content.decode(encoding, errors='ignore')
    # 以二进制模式写入文件
    with open(f'../outputFile/{out_file}', 'wb') as f:
        f.write(html_str.encode('utf-8'))


# 制作3个文件夹来存放网页
folder_names = ['j1', 'j2', 'j3']
parent_dir = '../outputFile'
# 遍历文件夹列表
for folder_name in folder_names:
    folder_path = os.path.join(parent_dir, folder_name)
    try:
        # 尝试创建文件夹
        os.mkdir(folder_path)
        print(f"成功创建文件夹: {folder_path}")
    except FileExistsError:
        print(f"文件夹 {folder_path} 已存在，无需创建。")

# 下载卷1(从01到25)
for i in range(1, 26):
    # 使用 zfill 方法将数字转换为宽度为 2 的字符串，不足的地方用 0 填充
    formatted_num = str(i).zfill(2)
    print(f"下载卷1 {formatted_num}")
    down_chapter(f"marx/capital/{formatted_num}.htm",
                 f'j1/{formatted_num}.html')

# 下载卷2(从003到023)
for i in range(3, 24):
    # 使用 zfill 方法将数字转换为宽度为 2 的字符串，不足的地方用 0 填充
    formatted_num = str(i).zfill(3)
    print(f"下载卷2 {formatted_num}")
    down_chapter(f"marx-engels/24/{formatted_num}.htm",
                 f'j2/{formatted_num}.html')

# 下载卷3(从002到053)
for i in range(2, 54):
    # 使用 zfill 方法将数字转换为宽度为 2 的字符串，不足的地方用 0 填充
    formatted_num = str(i).zfill(3)
    print(f"下载卷3 {formatted_num}")
    down_chapter(f"marx-engels/25/{formatted_num}.htm",
                 f'j3/{formatted_num}.html')
