"""
extract_controller_apis.py
扫描指定 Controller 目录，提取每个接口的中文名、完整路由及请求方法，输出到 CSV。

输出字段：java文件名, 接口中文名, 接口路由, 请求方法
"""
import re
import csv
from pathlib import Path

# ─── 配置 ───────────────────────────────────────────────────────────────────
CONTROLLER_DIR = Path(
    r"D:\proj\backend\ms-prod-center\ms-prod-core\src\main\java"
    r"\com\boot\prod\core\controller"
)
OUTPUT_CSV = Path(__file__).parent / "controller_apis_结果.csv"

# 排除的文件名列表（大小写不敏感匹配）
EXCLUDE_FILES = [
    "TranBusiToProcController.java",
    "SysUserInfoController.java",
    "BaseTmplQuestInfoController.java",
    "BaseTagInfoController.java",
    "BaseTagRelController.java",
    "BaseRuleDefInfoController.java",
    "BaseRuleElemRelController.java",
    "BaseRuleBusiRelController.java",
    "BaseQuestInfoController.java",
    "BaseQuestFillVariableRelController.java",
    "BaseProductStrategyController.java",
    "BaseIntfInfoController.java",
    "BaseCustRiskChkRelController.java",
    "RiskPaperController.java",
    "RiskQuestController.java",
    "RiskScoreController.java",
    "ProcNodeChnlItactvRuleController.java",
    "ProcNodeItemModLogController.java",
    "ProcNodeParamController.java",
    "ProcNodeRelController.java",
    "ProcReNodeController.java",
    "ProcRunInsController.java",
    "ProcRunNodeParamController.java",
    "BaseVariableController.java",
    "ProdFlowStageInsController.java",
    "ProdFlowStageController.java",
]

# 已知全局前缀常量映射（若有新常量在此补充）
KNOWN_PREFIXES = {
    "MsGeneralConsts.MS_API_PREFIX": "/api/v1",
}
# ────────────────────────────────────────────────────────────────────────────


def resolve_string(raw: str, static_fields: dict[str, str]) -> str:
    """
    将注解中的字符串值解析为纯字符串。
    支持形如 CONST + "/xxx" 或 "字面量" 的拼接表达式。
    同时支持 ClassName.FIELD_NAME 形式的引用（去掉类名前缀后查 static_fields）。
    """
    raw = raw.strip()
    # 先按 + 拆分各段
    parts = re.split(r'\s*\+\s*', raw)
    result = ""
    for part in parts:
        part = part.strip()

        # 1. 字符串字面量 "xxx"
        if part.startswith('"') and part.endswith('"'):
            result += part[1:-1]
            continue

        # 2. 已知全局常量（如 MsGeneralConsts.MS_API_PREFIX）
        matched = False
        for k, v in KNOWN_PREFIXES.items():
            if part == k:
                result += v
                matched = True
                break
        if matched:
            continue

        # 3. ClassName.FIELD_NAME 或 FIELD_NAME —— 在 static_fields 里查
        # 先尝试去掉"类名."前缀
        bare = re.sub(r'^\w+\.', '', part)  # 去掉 "BaseCellInfoController." 之类的前缀
        if bare in static_fields:
            result += static_fields[bare]
            continue
        # 也直接用原始名查
        if part in static_fields:
            result += static_fields[part]
            continue

        # 4. 实在不认识就原样追加（保留便于排查）
        result += part

    return result


def extract_static_fields(content: str) -> dict[str, str]:
    """提取类体内 static final String 字段，如 API_PREFIX = '/xxx'"""
    fields: dict[str, str] = {}
    # 匹配形如：static final String FOO = "bar";
    pattern = re.compile(
        r'static\s+final\s+String\s+(\w+)\s*=\s*([^;]+);'
    )
    for m in pattern.finditer(content):
        name = m.group(1)
        raw_val = m.group(2).strip()
        fields[name] = resolve_string(raw_val, {})
    return fields


def extract_class_prefix(content: str, static_fields: dict[str, str]) -> str:
    """提取类级 @RequestMapping 中的 value，作为接口路由前缀。"""
    # 匹配 @RequestMapping(value = ...) 在类声明之前（简单起见，取第一个匹配）
    # 兼容单属性写法 @RequestMapping("/xxx") 和多属性写法 @RequestMapping(value = ...)
    patterns = [
        # @RequestMapping(value = "xxx" + CONST, ...)
        re.compile(r'@RequestMapping\s*\(\s*value\s*=\s*([^,)]+(?:\+[^,)]+)*)'),
        # @RequestMapping("xxx")
        re.compile(r'@RequestMapping\s*\(\s*("(?:[^"\\]|\\.)*")\s*\)'),
    ]
    for pat in patterns:
        m = pat.search(content)
        if m:
            return resolve_string(m.group(1).strip(), static_fields)
    return ""


def extract_operation_summary(block: str) -> str:
    """从方法前的注解块中提取 @Operation(summary = "...") 的值。"""
    m = re.search(r'@Operation\s*\(\s*(?:[^)]*,\s*)?summary\s*=\s*"([^"]*)"', block)
    if m:
        return m.group(1)
    return ""


def _extract_annotation_inner(content: str, start_after: int) -> str:
    """
    从 '(' 开始（start_after 指向 '(' 的位置），向后匹配配对括号，
    返回括号内的完整内容（处理嵌套括号、多行）。
    """
    depth = 0
    buf = []
    for i in range(start_after, len(content)):
        ch = content[i]
        if ch == '(':
            depth += 1
            if depth == 1:
                continue          # 跳过最外层左括号本身
        elif ch == ')':
            depth -= 1
            if depth == 0:
                break             # 最外层右括号，结束
        if depth >= 1:
            buf.append(ch)
    return ''.join(buf)


def extract_method_route(block: str) -> tuple[str, str]:
    """
    从方法注解块中提取路由 value 和 HTTP 方法。
    返回 (route_suffix, http_method)。
    兼容：
      @GetMapping / @PostMapping / @PutMapping / @DeleteMapping / @PatchMapping
        - 无括号：@GetMapping（路由空串）
        - 直接字符串：@GetMapping("/path/{id}")
        - value= 形式：@GetMapping(value = "/path")
        - 数组形式：@GetMapping({"/path1", "/path2"})
      @RequestMapping(value=..., method=RequestMethod.GET)
    """
    short_map = {
        "Get": "GET",
        "Post": "POST",
        "Put": "PUT",
        "Delete": "DELETE",
        "Patch": "PATCH",
    }

    # --- 1. 快捷映射注解 ---
    # 先查有无括号，再决定如何解析
    short_no_paren = re.compile(
        r'@(Get|Post|Put|Delete|Patch)Mapping\s*(?![\s\w(]|\()'
    )
    short_with_paren = re.compile(
        r'@(Get|Post|Put|Delete|Patch)Mapping\s*\('
    )

    m = short_with_paren.search(block)
    if m:
        http_method = short_map[m.group(1)]
        paren_start = m.end() - 1      # 指向 '('
        inner = _extract_annotation_inner(block, paren_start)

        # 去掉注释和换行，方便后续匹配
        inner_clean = re.sub(r'//[^\n]*', '', inner)
        inner_clean = re.sub(r'\s+', ' ', inner_clean).strip()

        # value = "..." 或 value = {"...", "..."}
        val_m = re.search(r'value\s*=\s*(\{[^}]*}|"[^"]*"(?:\s*\+\s*"[^"]*")*|[\w.]+(?:\s*\+\s*[\w."]+)*)', inner_clean)
        if val_m:
            raw_val = val_m.group(1).strip()
            # 数组 {"a","b"} → 取第一个
            arr_m = re.search(r'"([^"]*)"', raw_val)
            if raw_val.startswith('{') and arr_m:
                return arr_m.group(1), http_method
            return resolve_string(raw_val, {}), http_method

        # 直接字符串 "/path" 或 "/path/{id}"
        str_m = re.search(r'"([^"]*)"', inner_clean)
        if str_m:
            return str_m.group(1), http_method

        # 数组但没有 value= 前缀：({"/a", "/b"})
        arr_direct = re.search(r'\{\s*"([^"]*)"', inner_clean)
        if arr_direct:
            return arr_direct.group(1), http_method

        # 括号内是常量引用
        const_m = re.search(r'^([\w.]+)$', inner_clean)
        if const_m:
            return resolve_string(const_m.group(1), {}), http_method

        return "", http_method

    # 无括号的 @GetMapping 等（紧接着换行/空白+public/访问修饰符/注解）
    m_no = re.compile(r'@(Get|Post|Put|Delete|Patch)Mapping\b').search(block)
    if m_no:
        return "", short_map[m_no.group(1)]

    # --- 2. @RequestMapping —— 需从 method = RequestMethod.XXX 提取 HTTP 方法 ---
    req_m = re.compile(r'@RequestMapping\s*\(').search(block)
    if req_m:
        paren_start = req_m.end() - 1
        inner = _extract_annotation_inner(block, paren_start)
        inner_clean = re.sub(r'//[^\n]*', '', inner)
        inner_clean = re.sub(r'\s+', ' ', inner_clean).strip()

        # 路由 value
        route = ""
        val_m = re.search(r'value\s*=\s*(\{[^}]*}|"[^"]*"(?:\s*\+\s*"[^"]*")*|[\w.]+(?:\s*\+\s*[\w."]+)*)', inner_clean)
        if val_m:
            raw_val = val_m.group(1).strip()
            arr_m = re.search(r'"([^"]*)"', raw_val)
            if raw_val.startswith('{') and arr_m:
                route = arr_m.group(1)
            else:
                route = resolve_string(raw_val, {})
        else:
            str_m = re.search(r'"([^"]*)"', inner_clean)
            if str_m:
                route = str_m.group(1)

        # HTTP 方法
        http_method = ""
        methods = re.findall(r'RequestMethod\.(\w+)', inner_clean)
        if methods:
            http_method = "/".join(methods)
        return route, http_method

    return "", ""


# 方法级映射注解正则（用于 split_method_blocks）
_METHOD_MAPPING_PAT = re.compile(
    r'@(?:(?:Get|Post|Put|Delete|Patch)Mapping|RequestMapping)\b'
)


def split_method_blocks(content: str) -> list[str]:
    """
    粗粒度地将文件内容按方法注解切割。
    每块 = 从某个 @Operation 或方法级映射注解开始，到下一个块开始之前。
    支持只有 @GetMapping 没有 @Operation 的接口。
    """
    # 收集所有 @Operation 和方法级 Mapping 注解的起始位置
    anchor_positions: list[int] = []

    for m in re.finditer(r'@Operation\s*\(', content):
        anchor_positions.append(m.start())

    # 方法级映射注解：只取不在类级 @RequestMapping 位置上的
    # 简单策略：取所有映射注解位置，去重、排序
    for m in _METHOD_MAPPING_PAT.finditer(content):
        anchor_positions.append(m.start())

    if not anchor_positions:
        return []

    # 去重、排序
    anchor_positions = sorted(set(anchor_positions))

    # 合并相邻的 @Operation 和紧跟的 @XxxMapping（同一方法块）
    # 策略：若两个锚点之间间距 < 500 字符（经验值），合并为同一块的起点取较小值
    merged: list[int] = []
    prev = anchor_positions[0]
    for cur in anchor_positions[1:]:
        if cur - prev < 600:
            # 同一方法块，保留更早的锚点
            pass
        else:
            merged.append(prev)
            prev = cur
    merged.append(prev)

    blocks: list[str] = []
    for i, start in enumerate(merged):
        end = merged[i + 1] if i + 1 < len(merged) else len(content)
        blocks.append(content[start:end])
    return blocks


def process_file(java_file: Path) -> list[tuple[str, str, str, str]]:
    """解析单个 Java 文件，返回 [(文件名, 中文名, 完整路由, 请求方法), ...]"""
    content = java_file.read_text(encoding="utf-8", errors="ignore")
    filename = java_file.name

    # 1. 提取类内静态字段
    static_fields = extract_static_fields(content)

    # 2. 类级路由前缀
    class_prefix = extract_class_prefix(content, static_fields)

    # 3. 切割方法块
    rows: list[tuple[str, str, str, str]] = []
    method_blocks = split_method_blocks(content)

    for block in method_blocks:
        summary = extract_operation_summary(block)
        method_route, http_method = extract_method_route(block)
        if summary or method_route:
            full_route = class_prefix + method_route
            rows.append((filename, summary, full_route, http_method))

    return rows


def main():
    all_rows: list[tuple[str, str, str, str]] = []

    java_files = sorted(CONTROLLER_DIR.glob("*.java"))

    # 过滤排除文件
    exclude_lower = {e.lower() for e in EXCLUDE_FILES}
    java_files = [jf for jf in java_files if jf.name.lower() not in exclude_lower]

    if exclude_lower:
        print(f"排除文件: {', '.join(EXCLUDE_FILES)}")
    print(f"共发现 {len(java_files)} 个 Java 文件，开始解析…")

    for jf in java_files:
        rows = process_file(jf)
        print(f"  {jf.name:<50s} => {len(rows)} 个接口")
        all_rows.extend(rows)

    # 写 CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["java文件名", "接口中文名", "接口路由", "请求方法"])
        writer.writerows(all_rows)

    print(f"\n[OK] 共提取 {len(all_rows)} 条接口，已写入：{OUTPUT_CSV}")


if __name__ == "__main__":
    main()
