# coding=utf-8
# @Time    : 2026/08/24
# @Software: PyCharm
"""
添加实体字段脚本

流程：
  1. 输入zip路径（不立即解压）
  2. 选择XML配置方式：生成样例 或 输入已有XML
  3. 生成样例XML到zip同级目录
  4. 循环要求输入xml路径，直到输入xml继续或0退出
  5. 确认后解压zip，解析XML添加字段
  6. 重新打包zip输出
"""

import os
import json
import shutil
from datetime import datetime
from typing import List, Tuple, Optional
from lxml import etree

from zip_util import unzip_file, zip_folder


def get_time_id(i: int) -> str:
    """用当前时间生成时间戳ID，格式如 2024030717275001"""
    now_time: str = datetime.now().strftime('%Y%m%d%H%M%S')
    return f"{now_time}0{i}"


def get_form_id_from_zip(zip_path: str) -> str:
    """直接从zip中读取desForm.json获取formId（不解压）"""
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as zf:
        content = zf.read('desForm.json').decode('utf-8')
        data = json.loads(content)
        if isinstance(data, list) and len(data) > 0:
            return data[0].get('formId', 'unknown')
    return 'unknown'


def generate_sample_xml(zip_path: str) -> str:
    """
    在zip同级目录生成字段样例XML文件
    :return: 生成的XML文件路径
    """
    # 获取zip基本信息
    form_id = get_form_id_from_zip(zip_path)
    xml_filename = f"fields_{form_id}.xml"
    xml_path = os.path.join(os.path.dirname(zip_path), xml_filename)

    xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!--
    字段追加配置文件
    field.code: 字段英文名（小驼峰命名）
    field.name: 字段中文名
    可添加多个field节点
-->
<tableList xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <table>
        <!-- 示例字段，请根据需要修改或删除 -->
        <field code="fieldCode" name="字段中文名"/>
    </table>
</tableList>'''

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    return xml_path


def parse_field_xml(xml_path: str) -> List[Tuple[str, str]]:
    """
    解析字段XML配置文件
    :return: [(field_code, field_name), ...]
    """

    fields = []
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # 查找所有 field 节点
    for table in root.findall('.//table'):
        for field in table.findall('field'):
            code = field.get('code')
            name = field.get('name')
            if code and name:
                fields.append((code, name))

    return fields


def get_entity_info(extract_dir: str) -> Tuple[str, str]:
    """
    从解压目录读取desBusEntity.json获取entityId和objectId
    :return: (entity_id, object_id)
    """
    bus_entity_path = os.path.join(extract_dir, "desBusEntity.json")
    if not os.path.exists(bus_entity_path):
        raise FileNotFoundError(f"zip中未找到desBusEntity.json：{bus_entity_path}")

    with open(bus_entity_path, 'r', encoding='utf-8') as f:
        bus_entity_data = json.load(f)

    if not isinstance(bus_entity_data, list) or len(bus_entity_data) == 0:
        raise ValueError("desBusEntity.json格式错误，应包含至少一个实体")

    entity_info = bus_entity_data[0]
    entity_id = entity_info.get('entityId', '')
    object_id = entity_info.get('objectId', '')

    if not entity_id or not object_id:
        raise ValueError("desBusEntity.json中缺少entityId或objectId")

    return entity_id, object_id


def get_existing_field_names(entity_field_data: list) -> set:
    """
    从desEntityField.json中提取已存在的字段名
    :return: fieldName的集合
    """
    return {item.get('fieldName', '') for item in entity_field_data if item.get('fieldName')}


def add_entity_field_process(
        zip_path: str,
        xml_path: str
) -> Optional[str]:
    """
    处理添加实体字段的核心逻辑

    :param zip_path: 表单zip文件路径
    :param xml_path: XML配置文件路径
    :return: 输出zip文件路径，失败返回None
    """
    print("=" * 50)
    print("  添加实体字段")
    print("=" * 50)

    # 解析XML获取字段列表
    try:
        fields = parse_field_xml(xml_path)
        if not fields:
            print("[错误] XML中未找到任何有效字段配置")
            return None
        print(f"\n解析到 {len(fields)} 个字段：")
        for code, name in fields:
            print(f"  - {code}: {name}")
    except Exception as e:
        print(f"[错误] 解析XML失败：{e}")
        return None

    # 解压zip
    print("\n--- 解压文件 ---")
    extract_dir = unzip_file(zip_path)

    try:
        # 获取entityId和objectId
        try:
            entity_id, object_id = get_entity_info(extract_dir)
            print(f"entityId：{entity_id}")
            print(f"objectId：{object_id}")
        except Exception as e:
            print(f"[错误] {e}")
            return None

        # 读取desEntityField.json
        entity_field_path = os.path.join(extract_dir, "desEntityField.json")
        if os.path.exists(entity_field_path):
            with open(entity_field_path, 'r', encoding='utf-8') as f:
                entity_field_data = json.load(f)
        else:
            entity_field_data = []
            print("[提示] desEntityField.json不存在，将创建新文件")

        # 获取已存在的字段名，用于去重
        existing_names = get_existing_field_names(entity_field_data)
        print(f"\n已存在 {len(existing_names)} 个字段")

        # 追加新字段（跳过已存在的）
        start_index = len(entity_field_data) + 1
        new_fields = []
        skipped_fields = []

        for i, (code, name) in enumerate(fields):
            if code in existing_names:
                skipped_fields.append((code, name))
                continue

            new_field_id = get_time_id(start_index + i)
            new_field = {
                "isNotNull": "0",
                "fieldName": code,
                "fieldNotes": name,
                "entityId": entity_id,
                "entityFieldType": "1",
                "objectId": object_id,
                "fieldId": new_field_id
            }
            entity_field_data.append(new_field)
            new_fields.append((new_field_id, code, name))
            existing_names.add(code)  # 防止XML中有重复字段

        # 报告结果
        if skipped_fields:
            print(f"\n跳过已存在的字段：")
            for code, name in skipped_fields:
                print(f"  - {code}: {name} (已存在)")

        if new_fields:
            print(f"\n已添加 {len(new_fields)} 个新字段：")
            for fid, code, name in new_fields:
                print(f"  + {code}: {name} (id={fid})")
        else:
            print("\n没有需要添加的新字段")
            return None

        # 写入desEntityField.json
        with open(entity_field_path, 'w', encoding='utf-8') as f:
            json.dump(entity_field_data, f, ensure_ascii=False, indent=2)
        print(f"\n已写入：{entity_field_path}")

        # 重新打包zip
        print("\n--- 重新压缩zip ---")
        zip_dir = os.path.dirname(zip_path) or "."
        zip_basename = os.path.splitext(os.path.basename(zip_path))[0]
        output_zip = os.path.join(zip_dir, zip_basename + "_with_field.zip")
        zip_folder(extract_dir, output_zip)

        print("\n[完成] 实体字段添加成功！")
        print(f"   输出文件：{output_zip}")

        return output_zip

    finally:
        # 清理临时解压目录
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir, ignore_errors=True)
            print(f"已清理临时目录：{extract_dir}")


def run(zip_path: str = None):
    """交互式入口
    """
    # 循环选择XML配置方式
    ask_num = 0
    while ask_num < 3:
        ask_num += 1
        print("\n请选择XML配置方式：")
        print("  1. 生成字段配置样例")
        print("  2. 输入已有XML文件路径")
        print("  0. 退出")
        choice = input("请选择 (1/2/0): ").strip()

        if choice == "0":
            print("已退出")
            return
        elif choice == "1":
            # 生成样例XML到zip同级目录
            xml_path = generate_sample_xml(zip_path)
            print(f"\n已生成字段配置样例：{xml_path}")
            print("请编辑该XML文件，添加需要的字段后保存。")
            # 生成后继续循环，让用户输入xml路径
            print()
        else:
            # 直接输入XML路径
            xml_path = input("请输入XML文件路径：").strip().strip('"').strip("'")
            if not xml_path:
                print("[错误] 未输入XML路径")
                continue
            # 执行添加字段
            add_entity_field_process(zip_path, xml_path)
            break
