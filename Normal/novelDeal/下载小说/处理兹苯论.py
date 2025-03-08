# coding=utf-8
# @Time    : 2025/2/18 20:21
# @Software: PyCharm
import os

from lxml import html, etree


def remove_attributes(element, attrs_to_remove):
    """从元素中移除属性
    """
    for attr in attrs_to_remove:
        if attr in element.attrib:
            del element.attrib[attr]


def remove_name_attributes_lxml(html_content):
    """解析html，并修改其中的标签
    """
    try:
        # 使用容错解析模式
        parser = etree.HTMLParser(recover=True)
        tree = html.fromstring(html_content, parser=parser)
        attrs_to_remove = ['name', 'size', 'color', 'align', 'width', 'border', 'cellspacing', 'cellpadding',
                           'style', 'valign']
        elements_to_remove = []
        for element in tree.iter():
            # 移除警告属性
            remove_attributes(element, attrs_to_remove)
            # 修改标签名字
            tag_name = element.tag.lower()
            if tag_name == 'p' and element.get('class') == 'title1':
                # 标题切换
                element.tag = 'h1'
            elif tag_name == 'h3':
                element.tag = 'h2'
            elif tag_name == 'h4':
                element.tag = 'h3'
            # 部分标签类联样式
            if tag_name == 'table' or tag_name == 'th' or tag_name == 'td':
                element.set('style', 'border: 1px solid black;')
            # 移除不需要标签
            if tag_name == 'a':
                elements_to_remove.append(element)
            elif tag_name == 'p' and element.get('class') == 'intr':
                elements_to_remove.append(element)  # 移除注释
            elif tag_name == 'img':
                elements_to_remove.append(element)
        # 最后统一删除
        for element in elements_to_remove:
            parent = element.getparent()
            if parent is not None:
                parent.remove(element)
        result = html.tostring(tree, encoding='unicode')
        # 移除不需要的font标签
        result = result.replace("<font>", "").replace("</font>", "")\
            .replace("<center>", "").replace("</center>", "")
        if result.startswith("<div>") and result.endswith("</div>"):
            result = result[5:-6]
        return result
    except Exception as e:
        print(f"处理 HTML 内容时发生错误: {e}")
        return html_content


def process_html_file(file_path):
    """删除html中的无关代码
    """
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 删除标题前的内容
        start_index = content.find("<p class='title1'>")
        if start_index != -1:
            content = content[start_index:]

        # 删除注释(脚注)
        end_index = content.find(
            "<hr color=\"#C0C0C0\" width=\"60%\" size=\"1\" align=\"left\"><span style=\"font-size: 10.5pt\">")
        if end_index != -1:
            content = content[:end_index]
        # 删除注释(以防万一)
        end_index = content.rfind("</body>")
        if end_index != -1:
            content = content[:end_index]

        # 对其中的属性进行处理
        new_html = remove_name_attributes_lxml(content)
        # 写入处理后的内容
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_html)

        print(f"处理完成: {file_path}")
    except Exception as e:
        print(f"处理文件 {file_path} 时出错: {e}")


def process_folder(folder_path, juan):
    # 遍历文件夹下的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                process_html_file(file_path)
    # 将文件夹下的html合并
    output_file = f"{os.path.dirname(folder_path)}/input{juan}.html"
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(f"""<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>卷{juan}</title>
</head>
<body>""")
        for filename in os.listdir(folder_path):
            if filename.endswith('.html'):
                with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as readfile:
                    # 写入文件内容
                    outfile.write(readfile.read())
        outfile.write("</body></html>")


if __name__ == "__main__":
    # 指定文件夹路径
    process_folder('../outputFile/j1', 1)
    process_folder('../outputFile/j2', 2)
    process_folder('../outputFile/j3', 3)
    # pandoc input.html -o output.epub
