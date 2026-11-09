# coding=utf-8
# @Time    : 2026/08/24
# @Software: PyCharm
"""
添加实体字段 + 表单字段脚本

实体字段与表单字段共用同一份 XML 配置，通过节点区分：
  <entityFields>  只加实体字段（写入 desEntityField.json）
  <formFields>    只加表单字段（写入 desFormControl.json + desFormLayout.json）
  两个节点都写      先加实体字段，再加表单字段

字段只读取 <field> 上的属性（code / name / controlType / generalDictionary /
customFieldName，以及可覆盖默认值的其它平台属性），不读取下级标签。

流程：
  1. 输入zip路径（不立即解压）
  2. 选择XML配置方式：生成样例 或 输入已有XML
  3. 生成样例XML到zip同级目录（样例内容从脚本目录 模板/field_sample.xml 读取）
  4. 循环要求输入xml路径，直到输入xml继续或0退出
  5. 确认后解压zip，解析XML添加字段
  6. 重新打包zip输出
"""

import os
import sys
import json
import shutil
from datetime import datetime
from typing import List, Tuple, Optional
from lxml import etree

import control_types
from zip_util import unzip_file, zip_folder

# 输出中文到控制台时避免 GBK 乱码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 样例XML模板位置：脚本目录下的 模板/field_sample.xml（不硬编码到代码中）
SCRIPT_DIR: str = os.path.dirname(os.path.abspath(__file__))
SAMPLE_TEMPLATE_PATH: str = os.path.join(SCRIPT_DIR, "模板", "field_sample.xml")


# ===================== 通用工具 =====================

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


# ===================== 样例XML生成 =====================

def generate_sample_xml(zip_path: str) -> str:
    """
    在zip同级目录生成字段配置样例XML文件。
    样例内容来自脚本目录下的 模板/field_sample.xml，不硬编码在代码里。

    :return: 生成的XML文件路径
    """
    if not os.path.exists(SAMPLE_TEMPLATE_PATH):
        raise FileNotFoundError(f"未找到样例模板：{SAMPLE_TEMPLATE_PATH}")

    form_id = get_form_id_from_zip(zip_path)
    xml_path = os.path.join(os.path.dirname(zip_path), f"fields_{form_id}.xml")

    with open(SAMPLE_TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)

    return xml_path


# ===================== XML 解析 =====================

class FormField(object):
    """字段配置项（只读取 <field> 上代码规定的几个属性）"""

    def __init__(self, code: str, name: str, control_type: str = '',
                 general_dictionary: str = '', custom_field_name: str = ''):
        self.code = code
        self.name = name
        self.control_type = control_type
        self.general_dictionary = general_dictionary
        self.custom_field_name = custom_field_name


def _parse_field_node(node) -> Optional[FormField]:
    """解析单个 <field> 节点，只读取 code / name / controlType / generalDictionary / customFieldName"""
    code = (node.get('code') or '').strip()
    if not code:
        return None
    name = (node.get('name') or '').strip() or code

    return FormField(
        code=code,
        name=name,
        control_type=(node.get('controlType') or '').strip(),
        general_dictionary=(node.get('generalDictionary') or '').strip(),
        custom_field_name=(node.get('customFieldName') or '').strip(),
    )


def parse_field_xml(xml_path: str) -> Tuple[List[FormField], List[FormField]]:
    """
    解析字段XML配置文件。

    :return: (实体字段列表, 表单字段列表)
    """
    parser = etree.XMLParser(remove_comments=False)
    tree = etree.parse(xml_path, parser)
    root = tree.getroot()

    entity_nodes = root.findall('.//entityFields')
    form_nodes = root.findall('.//formFields')

    if not entity_nodes and not form_nodes:
        raise ValueError(
            "XML 中未找到 entityFields 或 formFields 节点，请检查配置结构。"
        )

    entity_fields: List[FormField] = []
    for section in entity_nodes:
        for field_node in section.iter('field'):
            parsed = _parse_field_node(field_node)
            if parsed:
                entity_fields.append(parsed)

    form_fields: List[FormField] = []
    for section in form_nodes:
        for field_node in section.iter('field'):
            parsed = _parse_field_node(field_node)
            if parsed:
                form_fields.append(parsed)

    return entity_fields, form_fields


# ===================== 读取表单基础信息 =====================

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


def get_form_info(extract_dir: str) -> Tuple[str, str]:
    """
    从 desForm.json 读取 formId 和表单名
    :return: (form_id, form_name)
    """
    form_path = os.path.join(extract_dir, "desForm.json")
    if not os.path.exists(form_path):
        raise FileNotFoundError(f"zip中未找到desForm.json：{form_path}")

    with open(form_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("desForm.json格式错误，应包含至少一个表单")

    form_id = data[0].get('formId', '')
    form_name = data[0].get('formName', '') or data[0].get('formAlias', '')
    if not form_id:
        raise ValueError("desForm.json中缺少formId")
    return form_id, form_name


def load_json_list(path: str) -> list:
    """读取 JSON 列表文件，不存在时返回空列表"""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data if isinstance(data, list) else []


# ===================== 实体字段 =====================

def add_entity_fields(
        entity_field_data: list,
        fields: List[FormField],
        entity_id: str,
        object_id: str
) -> Tuple[list, list, list]:
    """
    向 desEntityField.json 数据中追加实体字段（跳过已存在的）。

    :return: (更新后的数据, 新增字段列表, 跳过字段列表)
    """
    existing_names = {item.get('fieldName', '') for item in entity_field_data if item.get('fieldName')}
    start_index = len(entity_field_data) + 1
    new_fields = []
    skipped_fields = []

    for i, field in enumerate(fields):
        if field.code in existing_names:
            skipped_fields.append(field)
            continue

        entity_field_data.append({
            "isNotNull": "0",
            "fieldName": field.code,
            "fieldNotes": field.name,
            "entityId": entity_id,
            "entityFieldType": "1",
            "objectId": object_id,
            "fieldId": get_time_id(start_index + i)
        })
        new_fields.append(field)
        existing_names.add(field.code)  # 防止XML中有重复字段

    return entity_field_data, new_fields, skipped_fields


# ===================== 表单字段 =====================

def _resolve_control_type(field: FormField) -> str:
    """
    确定表单字段的控件类型：
      1. 显式配置 controlType（支持中文）
      2. 配了字典 -> 默认下拉框
      3. 配了 customFieldName -> 自定义组件
      4. 否则默认输入框
    """
    value = field.control_type
    if value:
        return control_types.normalize_control_type(value)

    if field.general_dictionary:
        return control_types.DICT_DEFAULT_CONTROL_TYPE

    if field.custom_field_name:
        return "54"

    return control_types.DEFAULT_CONTROL_TYPE


def _guess_entity_field_name(bound_property: str, entity_names: List[str]) -> Optional[str]:
    """
    从绑定属性推断对应的实体字段名，例如 nodeInfo.isCirculate -> isCirculate。
    """
    if not bound_property:
        return None
    prop = bound_property.split('.')[-1].strip()
    return prop if prop in entity_names else None


def _find_root_layout(form_layout_data: list) -> Optional[dict]:
    """
    找出可作为新增字段容器的布局：
      1. layoutType == "101" 的根布局优先
      2. 否则取 parentLayoutId 不在本表单布局ID集合中的布局
      3. 再不行取第一个
    """
    if not form_layout_data:
        return None

    for item in form_layout_data:
        if str(item.get('layoutType', '')) == "101":
            return item

    all_ids = {item.get('layoutId') for item in form_layout_data}
    for item in form_layout_data:
        if item.get('parentLayoutId') not in all_ids:
            return item
    return form_layout_data[0]


def add_form_fields(control_data: list, layout_data: list, fields: List[FormField], form_id: str,
                    entity_names: List[str]) -> Tuple[list, list, list, list]:
    """
    向 desFormControl.json 追加表单字段（跳过已存在的 boundProperty）。

    :param control_data: desFormControl.json 数据
    :param layout_data:  desFormLayout.json 数据
    :param fields:       XML 中的表单字段配置
    :param form_id:      表单ID
    :param entity_names: 实体字段名集合（用于推断绑定属性对应的实体字段）
    :return: (control_data, layout_data, 新增字段, 跳过字段)
    """
    existing_props = {item.get('boundProperty', '') for item in control_data if item.get('boundProperty')}
    root_layout = _find_root_layout(layout_data)
    layout_id = root_layout.get('layoutId', '') if root_layout else ''
    start_order = len(control_data) + 1

    new_fields = []
    skipped_fields = []

    for i, field in enumerate(fields):
        bound_property = field.code
        if bound_property in existing_props:
            skipped_fields.append(field)
            continue

        control_type = _resolve_control_type(field)
        order = start_order + i

        control = control_types.build_control_defaults(control_type)
        control.update({
            "boundProperty": bound_property,
            "formId": form_id,
            "formFieldId": get_time_id(order),
            "layoutId": layout_id,
            "formFieldDescribe": field.name,
            "tableFieldOrder": order,
            # 未显式配置字典时，不输出 generalDictionary 键，避免空字典
            "generalDictionary": field.general_dictionary,
        })
        if not control["generalDictionary"]:
            control.pop("generalDictionary")

        # 自定义组件必须配置 customFieldName
        custom_field_name = field.custom_field_name
        if control_types.needs_custom_field_name(control_type):
            if not custom_field_name:
                entity_field = _guess_entity_field_name(bound_property, entity_names)
                custom_field_name = entity_field or bound_property.split('.')[-1]
                print(f"  [提示] 「{field.name}」未配置 customFieldName，"
                      f"已自动取「{custom_field_name}」")
            control["customFieldName"] = custom_field_name
        elif custom_field_name:
            control["customFieldName"] = custom_field_name

        control_data.append(control)
        new_fields.append((field, control_type, control.get("formFieldId")))
        existing_props.add(bound_property)

    return control_data, layout_data, new_fields, skipped_fields


# ===================== 主流程 =====================

def add_field_process(zip_path: str, xml_path: str) -> Optional[str]:
    """
    处理添加字段的核心逻辑（实体字段 + 表单字段）

    :param zip_path: 表单zip文件路径
    :param xml_path: XML配置文件路径
    :return: 输出zip文件路径，失败返回None
    """
    print("=" * 50)
    print("  添加实体字段 / 表单字段")
    print("=" * 50)

    # 解析XML
    try:
        entity_fields, form_fields = parse_field_xml(xml_path)
        if not entity_fields and not form_fields:
            print("[错误] XML 中未找到任何有效字段配置（entityFields / formFields 均为空）")
            print("       提示：<formFields> 默认是注释状态，需要加表单字段请先解开注释")
            return None
        print(f"\n解析到 实体字段 {len(entity_fields)} 个，表单字段 {len(form_fields)} 个")
    except Exception as e:
        print(f"[错误] 解析XML失败：{e}")
        return None

    # 解压zip
    print("\n--- 解压文件 ---")
    extract_dir = unzip_file(zip_path)

    try:
        try:
            entity_id, object_id = get_entity_info(extract_dir)
            form_id, form_name = get_form_info(extract_dir)
            print(f"formId：{form_id}（{form_name}）")
            print(f"entityId：{entity_id}")
            print(f"objectId：{object_id}")
        except Exception as e:
            print(f"[错误] {e}")
            return None

        entity_field_path = os.path.join(extract_dir, "desEntityField.json")
        control_path = os.path.join(extract_dir, "desFormControl.json")
        layout_path = os.path.join(extract_dir, "desFormLayout.json")

        entity_field_data = load_json_list(entity_field_path)
        control_data = load_json_list(control_path)
        layout_data = load_json_list(layout_path)

        if not os.path.exists(entity_field_path):
            print("[提示] desEntityField.json 不存在，将创建新文件")
        if not os.path.exists(control_path):
            print("[提示] desFormControl.json 不存在，将创建新文件")
        if not os.path.exists(layout_path):
            print("[提示] desFormLayout.json 不存在，将创建新文件")

        changed = False

        # ---------- 实体字段 ----------
        if entity_fields:
            print(f"\n--- 实体字段（已存在 {len(entity_field_data)} 个）---")
            entity_field_data, new_entity, skipped_entity = add_entity_fields(
                entity_field_data, entity_fields, entity_id, object_id
            )
            for field in skipped_entity:
                print(f"  - {field.code}: {field.name} (已存在，跳过)")
            for field in new_entity:
                print(f"  + {field.code}: {field.name}")
            if new_entity:
                with open(entity_field_path, 'w', encoding='utf-8') as f:
                    json.dump(entity_field_data, f, ensure_ascii=False, indent=2)
                print(f"已写入：{entity_field_path}")
                changed = True
            else:
                print("  没有需要添加的新实体字段")

        # ---------- 表单字段 ----------
        if form_fields:
            print(f"\n--- 表单字段（已存在 {len(control_data)} 个）---")
            entity_names = [item.get('fieldName', '') for item in entity_field_data]
            control_data, layout_data, new_form, skipped_form = add_form_fields(
                control_data, layout_data, form_fields, form_id, entity_names
            )
            for field in skipped_form:
                print(f"  - {field.code}: {field.name} (绑定属性已存在，跳过)")
            for field, ctrl_type, field_id in new_form:
                print(f"  + {field.code}: {field.name} "
                      f"[{control_types.control_type_name(ctrl_type)}] id={field_id}")
            if new_form:
                with open(control_path, 'w', encoding='utf-8') as f:
                    json.dump(control_data, f, ensure_ascii=False, indent=2)
                print(f"已写入：{control_path}")
                changed = True
            else:
                print("  没有需要添加的新表单字段")

        if not changed:
            print("\n[结束] 没有需要添加的新字段，未生成输出文件")
            return None

        # ---------- 重新打包 ----------
        print("\n--- 重新压缩zip ---")
        zip_dir = os.path.dirname(zip_path) or "."
        zip_basename = os.path.splitext(os.path.basename(zip_path))[0]
        output_zip = os.path.join(zip_dir, zip_basename + "_with_field.zip")
        zip_folder(extract_dir, output_zip)

        print("\n[完成] 字段添加成功！")
        print(f"   输出文件：{output_zip}")

        return output_zip

    finally:
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir, ignore_errors=True)
            print(f"已清理临时目录：{extract_dir}")


# ===================== 交互入口 =====================

def run(zip_path: str = None):
    """交互式入口"""
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
            try:
                xml_path = generate_sample_xml(zip_path)
                print(f"\n已生成字段配置样例：{xml_path}")
                print("请编辑该XML文件，添加需要的字段后保存。")
            except Exception as e:
                print(f"[错误] 生成样例失败：{e}")
            print()
        else:
            xml_path = input("请输入XML文件路径：").strip().strip('"').strip("'")
            if not xml_path:
                print("[错误] 未输入XML路径")
                continue
            if not os.path.exists(xml_path):
                print(f"[错误] 文件不存在：{xml_path}")
                continue
            add_field_process(zip_path, xml_path)
            break


if __name__ == "__main__":
    zip_input = input("请输入表单zip文件路径：").strip().strip('"').strip("'")
    if zip_input and os.path.exists(zip_input):
        run(zip_input)
    else:
        print(f"[错误] 文件不存在：{zip_input}")
