# coding=utf-8
# @Time    : 2026/08/24
# @Software: PyCharm
"""
控件类型配置模块

集中维护 desFormControl.json 中 controlType 的中文名称、各类型的差异属性
以及字段的默认值，供「样例XML生成」与「字段写回」共用，避免两处硬编码不一致。

XML 中可直接用中文配置组件形式，例如：
    <field code="nodeNm" name="节点名称" controlType="输入框"/>
    <field code="inlStat" name="初始状态" controlType="下拉框" generalDictionary="1160584000159485952"/>
    <field code="classifyId" name="所属阶段" controlType="自定义组件" customFieldName="lifeNodeStgId"/>
"""

from typing import Dict, List

# ===================== 控件类型中文 -> 编码 =====================

# 控件类型中文 -> 编码（只保留标准写法与编码本身）
CONTROL_TYPE_ALIASES: Dict[str, str] = {
    "1": "1",
    "输入框": "1",
    "2": "2",
    "多行文本": "2",
    "3": "3",
    "数字框": "3",
    "4": "4",
    "下拉框": "4",
    "5": "5",
    "单选框": "5",
    "54": "54",
    "自定义组件": "54",
}

# 编码 -> 规范中文名（用于日志与样例注释）
CONTROL_TYPE_NAMES: Dict[str, str] = {
    "1": "输入框",
    "2": "多行文本",
    "3": "数字框",
    "4": "下拉框",
    "5": "单选框",
    "54": "自定义组件",
}

# 使用字典的控件类型：配置了字典却没指定组件形式时，默认用下拉框
DICT_DEFAULT_CONTROL_TYPE = "4"

# 需要 customFieldName 的控件类型
CUSTOM_FIELD_CONTROL_TYPES = {"54"}


# ===================== 字段默认值 =====================

# 新增控件条目的默认基础属性（与平台导出一致）
BASE_CONTROL_DEFAULTS: Dict[str, object] = {
    "isSupportMultiple": "0",
    "dateFormat": "YYYY-MM-DD",
    "isPasswordBox": "0",
    "dynamicOptionType": "1",
    "isHideControl": "0",
    "isHideTitle": "0",
    "isOptionType": "2",
    "isClearButton": "0",
    "thousandthPercentileFormat": "0",
    "hiddenDropdown": "0",
    "isSearchable": "0",
    "formatType": "1",
    "fieldDefaultValue": "\"\"",
    "isBoldTitle": "0",
    "isLineFeedDisplay": "0",
    "verificationRules": "[]",
    "textFold": "0",
    "supportUploadType": "1",
    "busAttr": "{\"submittedType\":\"\",\"isSupplement\":false,\"isKeyElements\":false,\"isTrack\":false}",
    "canAddEntry": "0",
    "disableNonLeafNodes": "0",
    "enableAutoComplete": "0",
    "isMultipleChoice": "0",
    "isShowCapitalization": "0",
    "timeFormat": "HH:mm:ss",
    "moneyUnit": "[]",
    "isFixedRowHeight": "0",
    "isNotEdit": "0",
}

# 按控件类型追加的差异属性（同样与平台导出一致）
CONTROL_TYPE_DEFAULTS: Dict[str, Dict[str, object]] = {
    # 输入框：带标题宽度
    "1": {"titleWidth": "120px"},
    # 多行文本：带标题宽度
    "2": {"titleWidth": "120px"},
    # 数字：带最小值
    "3": {"titleWidth": "120px", "minValue": 1},
    # 下拉框 / 单选框 / 自定义组件：导出样例中均无 titleWidth，保持一致
    "4": {},
    "5": {},
    "54": {},
}

# 新增字段时默认选择的控件类型
DEFAULT_CONTROL_TYPE = "1"


# ===================== 对外方法 =====================

def normalize_control_type(value: str) -> str:
    """
    把 XML 中写的组件形式（中文名或编码）统一为 controlType 编码。

    :param value: 中文名（如「下拉框」）或编码（如 "4"）
    :return: controlType 编码
    :raises ValueError: 无法识别时抛出
    """
    key = (value or "").strip()
    if not key:
        raise ValueError("controlType 不能为空")

    # 全角/半角数字统一
    key = key.replace("（", "(").replace("）", ")")
    code = CONTROL_TYPE_ALIASES.get(key)
    if code is None:
        # 允许直接抄英文控件名（大小写不敏感）
        lower_map = {k.lower(): v for k, v in CONTROL_TYPE_ALIASES.items() if k.isascii()}
        code = lower_map.get(key.lower())

    if code is None:
        supported = "、".join(f"{k}({v})" for k, v in CONTROL_TYPE_NAMES.items())
        raise ValueError(f"无法识别的组件形式「{value}」，支持：{supported}")
    return code


def control_type_name(code: str) -> str:
    """编码 -> 中文名，未知编码原样返回"""
    return CONTROL_TYPE_NAMES.get(str(code), f"未知({code})")


def build_control_defaults(control_type: str) -> Dict[str, object]:
    """
    生成指定控件类型的基础属性字典（深拷贝，调用方可随意改写）。
    """
    data: Dict[str, object] = dict(BASE_CONTROL_DEFAULTS)
    data.update(CONTROL_TYPE_DEFAULTS.get(control_type, {}))
    data["controlType"] = control_type
    return data


def needs_custom_field_name(control_type: str) -> bool:
    """该控件类型是否必须配置 customFieldName"""
    return control_type in CUSTOM_FIELD_CONTROL_TYPES


def supported_control_type_hints() -> List[str]:
    """样例 XML 注释里展示的可选值列表"""
    return [f"{code}={name}" for code, name in CONTROL_TYPE_NAMES.items()]
