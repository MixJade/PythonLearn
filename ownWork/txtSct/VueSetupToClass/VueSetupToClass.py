# coding=utf-8
# @Time    : 2026/5/12 15:59
# @Software: PyCharm
"""
VueSetupToClass.py
=====================
将 vue-class-component + setup() 混用风格的 .vue 文件
自动迁移为纯 vue-class 风格（去除 setup，保留 @Options/@Prop 装饰器）。

迁移覆盖四个改动点：
  1. 响应式数据迁移   ref<T>(init) / reactive([...]) → 类成员属性（含类型注解）
  2. 生命周期迁移     onMounted / onUnmounted / ... → mounted() / unmounted() / ...
  3. proxy 替换      proxy.xxx → this.xxx
  4. 业务方法迁移     setup 内的箭头函数 → 类成员方法

import 清理：
  - 移除 setup / getCurrentInstance / onMounted 等仅在 setup 中使用的导入
  - 保留其余 vue-class-component / vue / 业务 import
"""

import re
import sys
from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# 常量
# ─────────────────────────────────────────────────────────────────────────────

# Composition API 生命周期钩子 → 类方法名映射
LIFECYCLE_MAP = {
    "onMounted": "mounted",
    "onUnmounted": "unmounted",
    "onBeforeMount": "beforeMount",
    "onBeforeUnmount": "beforeUnmount",
    "onUpdated": "updated",
    "onBeforeUpdate": "beforeUpdate",
    "onCreated": "created",
    "onActivated": "activated",
    "onDeactivated": "deactivated",
    "onErrorCaptured": "errorCaptured",
}

# setup 专属导入关键字（出现在 import { ... } from 'vue' 中需要移除的）
SETUP_ONLY_IMPORTS = {
    "setup",
    "getCurrentInstance",
    "ref",
    "reactive",
    "computed",
    "watch",
    "watchEffect",
    "toRef",
    "toRefs",
    *LIFECYCLE_MAP.keys(),
}

# vue-class-component 中 setup 函数也需从导入列表移除
VCC_REMOVE_IMPORTS = {"setup"}


# ─────────────────────────────────────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────────────────────────────────────

def find_matching_brace(text: str, start: int) -> int:
    """从 start 位置（应为 '{' 处）找到对应的 '}' 索引。"""
    depth = 0
    i = start
    in_str_single = False
    in_str_double = False
    in_template = False  # 模板字符串
    while i < len(text):
        ch = text[i]
        # 字符串处理（简单版，忽略转义边界情况）
        if ch == "'" and not in_str_double and not in_template:
            in_str_single = not in_str_single
        elif ch == '"' and not in_str_single and not in_template:
            in_str_double = not in_str_double
        elif ch == "`" and not in_str_single and not in_str_double:
            in_template = not in_template
        elif not in_str_single and not in_str_double and not in_template:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def indent_block(text: str, spaces: int) -> str:
    """对多行文本整体增加缩进。"""
    pad = " " * spaces
    lines = text.split("\n")
    return "\n".join(pad + line if line.strip() else line for line in lines)


# ─────────────────────────────────────────────────────────────────────────────
# 核心：提取 setup() 块
# ─────────────────────────────────────────────────────────────────────────────

def extract_setup_body(script: str):
    """
    找到 `listData = setup(() => { ... })` 或 `setup(() => { ... })`
    返回 (setup_full_match_start, setup_full_match_end, body_str)
    body_str 是最外层花括号内的内容（不含首尾大括号）
    """
    # 匹配 `xxx = setup(() => {` 或直接 `setup(() => {`
    pattern = re.compile(
        r'(?:[\w$]+ \s*=\s*)? setup\s*\(\s*\(\s*\)\s*=>\s*\{',
        re.DOTALL
    )
    m = pattern.search(script)
    if not m:
        # 也尝试 setup(() => { 无赋值形式
        pattern2 = re.compile(r'setup\s*\(\s*\(\s*\)\s*=>\s*\{', re.DOTALL)
        m = pattern2.search(script)
    if not m:
        return None, None, None

    # 找到 setup 箭头函数体的起始大括号
    brace_start = script.index("{", m.start())
    brace_end = find_matching_brace(script, brace_start)
    if brace_end == -1:
        raise ValueError("找不到 setup() 的闭合括号 '}'")

    # setup(...) 的整个调用到 ')' 结束（brace_end + 1 是 '}', 之后是 ')'）
    # 需要找 setup( ... ) 的最外层括号
    paren_start_idx = script.index("(", m.start() + script[m.start():].index("setup"))
    # 找 setup((...) => {...}) 的外层括号结束
    paren_end = find_matching_paren(script, paren_start_idx)

    body = script[brace_start + 1: brace_end]
    # 整段赋值语句的范围（含行尾分号）
    stmt_start = m.start()
    # 找到完整语句末尾（paren_end 之后可能有 ';' 或换行）
    stmt_end = paren_end + 1
    if stmt_end < len(script) and script[stmt_end] == ";":
        stmt_end += 1

    return stmt_start, stmt_end, body


def find_matching_paren(text: str, start: int) -> int:
    """从 start（'(' 处）找到对应 ')' 的位置。"""
    depth = 0
    i = start
    in_str_single = False
    in_str_double = False
    in_template = False
    while i < len(text):
        ch = text[i]
        if ch == "'" and not in_str_double and not in_template:
            in_str_single = not in_str_single
        elif ch == '"' and not in_str_single and not in_template:
            in_str_double = not in_str_double
        elif ch == "`" and not in_str_single and not in_str_double:
            in_template = not in_template
        elif not in_str_single and not in_str_double and not in_template:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


# ─────────────────────────────────────────────────────────────────────────────
# 迁移点 1：响应式数据 → 类成员属性
# ─────────────────────────────────────────────────────────────────────────────

def parse_ref_declarations(body: str) -> list[dict]:
    """
    解析 body 中所有 ref<T>(init) / ref(init) 声明。
    支持嵌套泛型：ref<Array<string>>(...)
    返回列表 [{name, type_ann, init_expr, comment, full_start, full_end}, ...]
    """
    results = []
    # 先找 const name = ref
    pattern = re.compile(
        r'(?P<comment>//[^\n]*)?\n?\s*'
        r'const\s+(?P<name>\w+)\s*=\s*ref'
    )
    for m in pattern.finditer(body):
        name = m.group("name")
        comment = (m.group("comment") or "").strip()
        after = m.end()

        # 解析泛型参数（支持嵌套）
        generic_str = ""
        if after < len(body) and body[after] == "<":
            gen_start = after
            gen_end = _find_generic_end(body, gen_start)
            generic_str = body[gen_start:gen_end]
            after = gen_end

        # 找 '('
        while after < len(body) and body[after] in " \t\n":
            after += 1
        if after >= len(body) or body[after] != "(":
            continue

        paren_start = after
        paren_end = find_matching_paren(body, paren_start)
        init_expr = body[paren_start + 1: paren_end].strip()

        # 推导 TS 类型注解
        type_ann = _infer_type(generic_str, init_expr)

        results.append({
            "name": name,
            "type_ann": type_ann,
            "init_expr": init_expr,
            "comment": comment,
            "full_start": m.start(),
            "full_end": paren_end + 1,
        })
    return results


def _find_generic_end(text: str, start: int) -> int:
    """
    从 start 位置（指向 reactive 后的 '<'）开始，
    正确匹配嵌套的 TypeScript 泛型参数，返回泛型结束位置的下一个字符。
    例如: reactive<Partial<AccountCloseApply>>(
                   ^start              ^返回的位置（指向最后一个 > 之后）
    """
    i = start
    depth = 0
    while i < len(text):
        ch = text[i]
        if ch == "<":
            depth += 1
        elif ch == ">":
            depth -= 1
            if depth == 0:
                return i + 1  # 返回 '>' 之后的位置
        i += 1
    return start


def parse_reactive_declarations(body: str) -> list[dict]:
    """
    解析 body 中所有 reactive([...]) / reactive({...}) 声明。
    支持有无泛型参数两种形式：reactive(...) 和 reactive<T>(...)
    支持嵌套泛型：reactive<Partial<T>>(...)
    返回列表 [{name, type_ann, init_expr, comment, full_start, full_end}, ...]
    """
    results = []
    pattern = re.compile(
        r'(?P<comment>//[^\n]*)?\n?\s*'
        r'const\s+(?P<name>\w+)\s*=\s*reactive'
    )
    for m in pattern.finditer(body):
        name = m.group("name")
        comment = (m.group("comment") or "").strip()
        after = m.end()

        # 解析泛型参数（支持嵌套）
        type_ann = "any"
        if after < len(body) and body[after] == "<":
            gen_start = after
            gen_end = _find_generic_end(body, gen_start)
            type_ann = body[gen_start + 1: gen_end - 1].strip()  # 去掉 < 和 >
            after = gen_end

        # 跳过空格，寻找 '('
        while after < len(body) and body[after] in " \t\n":
            after += 1

        if after < len(body) and body[after] == "(":
            paren_start = after
            paren_end = find_matching_paren(body, paren_start)
            init_expr = body[paren_start + 1: paren_end].strip()
            results.append({
                "name": name,
                "type_ann": type_ann,
                "init_expr": init_expr,
                "comment": comment,
                "full_start": m.start(),
                "full_end": paren_end + 1,
            })
    return results


def _infer_type(generic: str, init_expr: str) -> str:
    """根据泛型注解和初始值推断 TS 类型。"""
    if generic:
        inner = generic.strip("<>")
        return inner  # e.g. any / any[] / string
    # 无泛型时根据初始值猜测
    init = init_expr.strip()
    if init == "[]":
        return "any[]"
    if init in ("null", "undefined"):
        return "any"
    if init.startswith("["):
        return "any[]"
    if init.startswith("{"):
        return "any"
    if init.startswith('"') or init.startswith("'") or init.startswith("`"):
        return "string"
    if re.match(r'^-?\d+(\.\d+)?$', init):
        return "number"
    if init in ("true", "false"):
        return "boolean"
    return "any"


def build_class_member_from_ref(info: dict, indent: int = 2) -> str:
    """生成类成员属性代码行。"""
    pad = " " * indent
    comment_line = f"{pad}{info['comment']}\n" if info["comment"] else ""
    type_part = f": {info['type_ann']}" if info["type_ann"] not in ("", "any") else ": any"
    # 如果 type_ann 是 any 且 init 看起来不是简单值，去掉类型注解（让 TS 推断）
    if info["type_ann"] == "any" and not re.match(r'^[\[\]{}\'"` ]', info["init_expr"]):
        type_part = ": any"
    # 如果 init_expr 为空（如 ref<any>()），生成 `name: any;` 而非 `name: any = ;`
    if info["init_expr"]:
        return f"{comment_line}{pad}{info['name']}{type_part} = {info['init_expr']};"
    else:
        return f"{comment_line}{pad}{info['name']}{type_part};"


# ─────────────────────────────────────────────────────────────────────────────
# 迁移点 2：生命周期
# ─────────────────────────────────────────────────────────────────────────────

def extract_lifecycle_hooks(body: str) -> list[dict]:
    """
    提取 body 中所有生命周期钩子调用：
    onMounted(() => { ... }) → {hook_name, class_method, body_content, full_start, full_end}
    """
    results = []
    hook_pattern = re.compile(
        r'(' + "|".join(re.escape(k) for k in LIFECYCLE_MAP) + r')\s*\(\s*\(\s*\)\s*=>\s*\{'
    )
    for m in hook_pattern.finditer(body):
        hook = m.group(1)
        brace_start = body.index("{", m.start())
        brace_end = find_matching_brace(body, brace_start)
        hook_body = body[brace_start + 1: brace_end]

        # 找到完整调用结束 ')'
        paren_start = body.index("(", m.start())
        paren_end = find_matching_paren(body, paren_start)

        results.append({
            "hook_name": hook,
            "class_method": LIFECYCLE_MAP[hook],
            "body_content": hook_body,
            "full_start": m.start(),
            "full_end": paren_end + 1,
        })
    return results


def build_lifecycle_method(info: dict, indent: int = 2) -> str:
    """生成类生命周期方法代码。"""
    pad = " " * indent
    inner = info["body_content"].strip("\n")
    # 对方法体重新缩进
    inner_lines = inner.split("\n")
    indented_inner = "\n".join(pad + "  " + line if line.strip() else line for line in inner_lines)
    return f"{pad}{info['class_method']}() {{\n{indented_inner}\n{pad}}}"


# ─────────────────────────────────────────────────────────────────────────────
# 迁移点 3：proxy.xxx → this.xxx
# ─────────────────────────────────────────────────────────────────────────────

def replace_proxy_references(text: str) -> str:
    """
    将 proxy.xxx 替换为 this.xxx，并移除 proxy 变量声明行。
    支持两种形式：
      - const proxy = getCurrentInstance()?.proxy as this;
      - const { proxy } = getCurrentInstance() as any;
    """
    # 替换 proxy.xxx
    text = re.sub(r'\bproxy\.', 'this.', text)
    # 移除 `const proxy = getCurrentInstance()...` 或 `const { proxy } = getCurrentInstance()...`
    text = re.sub(r'\s*const\s+\{?\s*proxy\s*}?\s*=\s*getCurrentInstance\(\)[^\n]*\n', '\n', text)
    return text


# ─────────────────────────────────────────────────────────────────────────────
# 迁移点 4：业务方法（箭头函数 const fn = (...) => {...}）→ 类成员方法
# ─────────────────────────────────────────────────────────────────────────────

def extract_arrow_functions(body: str, skip_names: set = None) -> list[dict]:
    """
    提取 body 中所有 `const fnName = (params): ReturnType => { ... }` 形式。
    跳过已作为生命周期处理的名称（skip_names）。
    返回 [{name, params, return_type, body_content, comments, full_start, full_end}, ...]
    """
    skip_names = skip_names or set()
    results = []
    # 支持 JSDoc 多行注释 + 单行注释 + const fnName = (...): Type => {
    pattern = re.compile(
        r'(?P<jsdoc>/\*\*.*?\*/\s*)?'  # JSDoc
        r'(?P<line_comment>//[^\n]*\n\s*)?'  # 行注释
        r'const\s+(?P<name>\w+)\s*=\s*'
        r'\((?P<params>[^)]*)\)'
        r'(?:\s*:\s*(?P<ret>[^=>{]+?))?'  # 可选返回类型
        r'\s*=>\s*\{',
        re.DOTALL
    )
    for m in pattern.finditer(body):
        name = m.group("name")
        if name in skip_names:
            continue
        params = m.group("params").strip()
        ret_type = (m.group("ret") or "").strip()
        jsdoc = (m.group("jsdoc") or "").strip()
        line_comment = (m.group("line_comment") or "").strip()

        brace_start = body.index("{", m.end() - 1)
        brace_end = find_matching_brace(body, brace_start)
        fn_body = body[brace_start + 1: brace_end]

        # 完整语句末尾（含 ';'）
        stmt_end = brace_end + 1
        if stmt_end < len(body) and body[stmt_end] == ";":
            stmt_end += 1

        results.append({
            "name": name,
            "params": params,
            "return_type": ret_type,
            "jsdoc": jsdoc,
            "line_comment": line_comment,
            "body_content": fn_body,
            "full_start": m.start(),
            "full_end": stmt_end,
        })
    return results


def build_class_method(info: dict, indent: int = 2) -> str:
    """生成类成员方法代码。"""
    pad = " " * indent
    ret = f": {info['return_type']}" if info["return_type"] else ""
    params = info["params"]
    inner = info["body_content"].strip("\n")
    inner_lines = inner.split("\n")
    indented_inner = "\n".join(pad + "  " + line if line.strip() else line for line in inner_lines)

    parts = []
    if info["jsdoc"]:
        # 重新对齐 JSDoc
        jsdoc_lines = info["jsdoc"].split("\n")
        parts.append("\n".join(pad + line.strip() for line in jsdoc_lines))
    if info["line_comment"]:
        parts.append(f"{pad}{info['line_comment']}")
    parts.append(f"{pad}{info['name']}({params}){ret} {{")
    parts.append(indented_inner)
    parts.append(f"{pad}}}")
    return "\n".join(parts)


# ─────────────────────────────────────────────────────────────────────────────
# import 清理
# ─────────────────────────────────────────────────────────────────────────────

def clean_imports(script: str) -> str:
    """
    1. 从 'vue' 的 import { ... } 中移除 SETUP_ONLY_IMPORTS 中的标识符
    2. 从 'vue-class-component' 的 import { ... } 中移除 VCC_REMOVE_IMPORTS
    3. 如果某条 import {} 清空了，删除整行
    """

    def _remove_from_named_import(line2: str, to_remove: set) -> str:
        """从 import { a, b, c } from '...' 中移除 to_remove 中的标识符。"""
        m = re.match(r'^(\s*import\s*\{)([^}]+)(}\s*from\s*.+)$', line2)
        if not m:
            return line2
        names = [n.strip() for n in m.group(2).split(",")]
        filtered = [n for n in names if n and n not in to_remove]
        if not filtered:
            return ""  # 整行删除
        return m.group(1) + " " + ", ".join(filtered) + " " + m.group(3)

    lines = script.split("\n")
    result = []
    for line in lines:
        # vue 导入
        if re.search(r'from\s+["\']vue["\']', line) and "import" in line and "{" in line:
            new_line = _remove_from_named_import(line, SETUP_ONLY_IMPORTS)
            if new_line:
                result.append(new_line)
            # 空行则跳过
        # vue-class-component 导入
        elif re.search(r'from\s+["\']vue-class-component["\']', line) and "{" in line:
            new_line = _remove_from_named_import(line, VCC_REMOVE_IMPORTS)
            if new_line:
                result.append(new_line)
        else:
            result.append(line)
    return "\n".join(result)


# ─────────────────────────────────────────────────────────────────────────────
# return 语句处理（去除 setup 的 return { ... }）
# ─────────────────────────────────────────────────────────────────────────────

def remove_return_statement(body: str) -> str:
    """移除 setup body 末尾的 return { ... }; 语句。"""
    # 找最后一个 return {
    m = list(re.finditer(r'\breturn\s*\{', body))
    if not m:
        return body
    last = m[-1]
    brace_start = body.index("{", last.start())
    brace_end = find_matching_brace(body, brace_start)
    # 去掉 return {...}; 包括前后空白行
    before = body[:last.start()].rstrip()
    after = body[brace_end + 1:]
    # 去掉尾部可能的 ';'
    after = after.lstrip(";").lstrip("\n")
    return before + "\n" + after


# ─────────────────────────────────────────────────────────────────────────────
# 辅助：为类成员裸引用加 this. 前缀
# ─────────────────────────────────────────────────────────────────────────────

def _add_this_prefix(script: str, member_names: set[str]) -> str:
    """
    在类方法体内，将对 member_names 中标识符的裸引用替换为 this.xxx。
    支持两种形式：
      - 裸标识符：formData → this.formData
      - 链式访问：formData.closeAccList → this.formData.closeAccList
    """
    if not member_names:
        return script

    sorted_names = sorted(member_names, key=len, reverse=True)

    # 找到类体的字符范围
    class_m = re.search(r'export default class \w+ extends Vue \{', script)
    if not class_m:
        return script
    class_brace_start = script.index("{", class_m.start())
    class_brace_end = find_matching_brace(script, class_brace_start)
    class_body = script[class_brace_start + 1: class_brace_end]

    def process_class_body(body: str) -> str:
        lines = body.split("\n")
        result = []
        for line in lines:
            stripped = line.lstrip()
            # 跳过空行、注释行、JSDoc
            if not stripped or stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
                result.append(line)
                continue
            # 计算缩进
            indent_spaces = len(line) - len(line.lstrip(" "))
            # 类成员定义行（缩进==2，方法/属性/装饰器签名），不做 this. 替换
            is_def_line = (
                    indent_spaces == 2
                    and bool(re.match(r'\s{2}[@\w$][\w$]*\s*[(:={]', line))
                    and not stripped.startswith("this.")
                    and not stripped.startswith("return ")
                    and not stripped.startswith("if ")
                    and not stripped.startswith("for ")
                    and not stripped.startswith("while ")
            )
            if is_def_line:
                result.append(line)
                continue
            # 对方法体内部行做两轮替换
            # 第一轮：裸标识符 → this.ident
            for name in sorted_names:
                # 不替换已有 this.xxx / proxy.xxx / 对象键 "name:"
                pattern = r'(?<!\bthis\.)(?<!\bproxy\.)(?<![.\w$])\b' + re.escape(name) + r'\b(?!\s*:(?!:))'
                line = re.sub(pattern, f'this.{name}', line)
            # 第二轮：成员.属性 → this.成员.属性（如 formData.xxx → this.formData.xxx）
            for name in sorted_names:
                pattern = r'(?<!\bthis\.)(?<!\bproxy\.)\b' + re.escape(name) + r'(\.[\w$][\w$.]*)'
                line = re.sub(pattern, rf'this.{name}\1', line)
            result.append(line)
        return "\n".join(result)

    new_class_body = process_class_body(class_body)
    return script[:class_brace_start + 1] + new_class_body + script[class_brace_end:]


# ─────────────────────────────────────────────────────────────────────────────
# 主转换逻辑
# ─────────────────────────────────────────────────────────────────────────────

def transform_script(script: str) -> str:
    """
    对 <script> 标签内容做全部迁移。
    """

    # ── Step 0: 先替换 proxy.xxx → this.xxx ──────────────────────────────────
    script = replace_proxy_references(script)

    # ── Step 1: 定位 setup() 块 ───────────────────────────────────────────────
    setup_start, setup_end, setup_body = extract_setup_body(script)
    if setup_start is None:
        print("[INFO] 未找到 setup() 块，文件无需迁移。")
        return script

    # ── Step 2: 从 setup body 中提取各类声明 ─────────────────────────────────

    # 2a. 响应式数据（ref + reactive）
    ref_decls = parse_ref_declarations(setup_body)
    reactive_decls = parse_reactive_declarations(setup_body)
    all_data_names = {d["name"] for d in ref_decls + reactive_decls}

    # 2b. 生命周期钩子
    lifecycle_hooks = extract_lifecycle_hooks(setup_body)
    lifecycle_names = set()  # 生命周期钩子本身不是 const 函数，不会重复

    # 2c. 箭头函数（业务方法），跳过已处理的数据名
    skip = all_data_names | lifecycle_names
    arrow_fns = extract_arrow_functions(setup_body, skip_names=skip)

    # ── Step 3: 构造要插入到类体中的代码块 ───────────────────────────────────
    class_members = []

    # 类成员属性（响应式数据）
    for d in ref_decls:
        class_members.append(build_class_member_from_ref(d))
    for d in reactive_decls:
        class_members.append(build_class_member_from_ref(d))

    # 生命周期方法
    for h in lifecycle_hooks:
        class_members.append(build_lifecycle_method(h))

    # 业务方法
    for fn in arrow_fns:
        class_members.append(build_class_method(fn))

    new_members_block = "\n\n".join(class_members)

    # ── Step 4: 从脚本中删除 setup() 整段，插入类成员到类体末尾 ──────────────

    # 4a. 删除 setup 语句（含 listData = setup(...)）
    script = script[:setup_start] + script[setup_end:]

    # 4b. 找到类定义的末尾 '}'（文件中最后一个顶层 '}'）
    # 查找 "export default class Xxx extends Vue {" 的位置
    class_m = re.search(r'export default class \w+ extends Vue \{', script)
    if not class_m:
        print("[WARN] 找不到 'export default class ... extends Vue {'，跳过插入。")
        return script

    class_brace_start = script.index("{", class_m.start())
    class_brace_end = find_matching_brace(script, class_brace_start)

    # 在类的闭合括号前插入新成员
    insert_pos = class_brace_end
    before_insert = script[:insert_pos].rstrip()
    after_insert = script[insert_pos:]

    script = before_insert + "\n\n" + new_members_block + "\n" + after_insert

    # ── Step 5: 替换 xxx.value → xxx（类成员不用 .value）───────────────────
    for name in all_data_names:
        script = re.sub(r'\b' + re.escape(name) + r'\.value\b', name, script)

    # ── Step 5b: 方法体内对类成员/方法的裸引用加 this. ──────────────────────
    # 收集所有需要加 this. 的标识符：响应式数据 + 业务方法名
    member_names = all_data_names | {fn["name"] for fn in arrow_fns}
    script = _add_this_prefix(script, member_names)

    # ── Step 6: 清理 import ──────────────────────────────────────────────────
    script = clean_imports(script)

    return script


# ─────────────────────────────────────────────────────────────────────────────
# .vue 文件分段处理
# ─────────────────────────────────────────────────────────────────────────────

def split_vue_file(content: str):
    """分离 template / script / style 三段。"""
    # 提取 <script ...>...</script>
    script_m = re.search(r'(<script[^>]*>)(.*?)(</script>)', content, re.DOTALL)
    if not script_m:
        raise ValueError("未找到 <script> 块")
    return (
        content[:script_m.start()],  # before (template)
        script_m.group(1),  # <script lang="ts">
        script_m.group(2),  # script body
        script_m.group(3),  # </script>
        content[script_m.end()],  # after (style)
    )


def process_vue_file(input_path: str):
    src = Path(input_path)
    if not src.exists():
        print(f"[ERROR] 文件不存在: {input_path}")
        sys.exit(1)

    content = src.read_text(encoding="utf-8")

    try:
        before, script_open, script_body, script_close, after = split_vue_file(content)
    except ValueError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    new_script_body = transform_script(script_body)

    new_content = before + script_open + new_script_body + script_close + after

    src.write_text(new_content, encoding="utf-8")
    print(f"[OK] 迁移完成 → {src}")


# ─────────────────────────────────────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(__doc__)
    input_file = input("请输入vue文件路径：").strip().strip('"')
    if input_file:
        process_vue_file(input_file)
