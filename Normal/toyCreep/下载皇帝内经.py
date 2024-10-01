# coding=utf-8
# @Time    : 2024/10/1 10:20
# @Software: PyCharm
import requests
import unicodedata
from lxml import etree

# noinspection SpellCheckingInspection
url = "https://www.gushiwen.cn/guwen/book.aspx?id=10"
base_url = "https://www.gushiwen.cn"
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
# 2. 请求 content：
html_str = requests.get(url, headers=ua).text
html_dom = etree.HTML(html_str)  # 将字符串转化为真正的 html
# 3. 删选数据 xpath
book_name: str = html_dom.xpath(
    '//div[contains(@id, "sonsyuanwen")]/div[contains(@class, "cont")]/h1/span/b/text()')[0]
print(f"书名{book_name}")

chapter_urls: list[str] = html_dom.xpath(
    '//div[contains(@class, "bookcont")]/div/span/a[contains(@href,"guwen")]/@href')
chapter_names: list[str] = html_dom.xpath(
    '//div[contains(@class, "bookcont")]/div/span/a[contains(@href,"guwen")]/text()')
print(f"共有{len(chapter_urls)}个url，{len(chapter_names)}个章节名")

book_content: str = f"""---
title: 《{book_name}》
language: zh-CN
---
"""

for i in range(len(chapter_urls)):
    print(f"下载：{i + 1} {chapter_names[i]}")
    chapter_dom = etree.HTML(requests.get(base_url + chapter_urls[i], headers=ua).text)
    # 章节内容，每一句都是一个元素，使用unicodedata的NFKC标准
    chapter_content: list[str] = chapter_dom.xpath(
        '//div[contains(@class, "sons")]/div[contains(@class, "cont")]/div[contains(@class, "contson")]/p/text()')
    book_content += f"\n\n# {i + 1} {chapter_names[i]}"
    for item in chapter_content:
        book_content += "\n\n" + unicodedata.normalize('NFKC', item)

# 最后统一写入
with open(f'../outputFile/{book_name}.md', 'w', encoding='utf-8') as f:
    f.write(book_content)
