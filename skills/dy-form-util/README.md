# 数据样例说明

本目录包含 dy-form-util 工具链所需的最小 JSON 样例数据。使用前需先用 `zip_util.py` 将三个 JSON 打包为 zip。

---

## 重要：zip 格式要求

工具链处理的 zip **必须是扁平的**，即解压后直接就是文件，不包含子文件夹：

```
# ✅ 正确：文件直接在 zip 根目录下
样例表单.zip
 ├── desForm.json
 ├── desFormControl.json
 ├── desFormLayout.json
 └── ...

# ❌ 错误：多了一层文件夹包裹
样例表单.zip
 └── 样例表单/               ← 多余的文件夹层！
      ├── desForm.json
      ├── desFormControl.json
      └── ...
```

> 从平台导出的 zip 通常就是扁平结构，注意不要用系统右键"压缩到 xxx/" 产生多余文件夹。

---

## 样例文件一览

### 1. desForm.json — 表单定义

顶层为**单元素数组**（多元素会被拒绝），含 `formId` 用于校验和移植匹配：

```json
[
  {
    "formId": "1234567890123456789",
    "formName": "SampleForm",
    "formType": "1",
    "formAlias": "样例表单",
    "useState": "1"
  }
]
```

### 2. desFormControl.json — 控件列表

共 **3 个控件**，分别演示三种场景：

```json
[
  {
    "formId": "1234567890123456789",
    "formFieldId": "ctrl_001",
    "layoutId": "layout_001",
    "formFieldDescribe": "机构名称",
    "boundProperty": "SampleForm.orgName",
    "generalDictionary": "",
    "treeShape": "",
    "controlType": "text"
  },
  {
    "formId": "1234567890123456789",
    "formFieldId": "ctrl_002",
    "layoutId": "layout_002",
    "formFieldDescribe": "资产分类",
    "boundProperty": "SampleForm.assetCategory",
    "generalDictionary": "9876543210987654321",
    "treeShape": "",
    "controlType": "select"
  },
  {
    "formId": "1234567890123456789",
    "formFieldId": "ctrl_003",
    "layoutId": "layout_003",
    "formFieldDescribe": "业务分类",
    "boundProperty": "SampleForm.bizCategory",
    "generalDictionary": "",
    "treeShape": "1122334455667788990",
    "controlType": "tree"
  }
]
```

| 控件 | 场景 |
|---|---|
| `ctrl_001` | 无字典、无树形（纯文本输入框） |
| `ctrl_002` | 有 `generalDictionary` 普通字典（下拉选择） |
| `ctrl_003` | 有 `treeShape` 树形字典（树形选择器） |

### 3. desFormLayout.json — 布局定义

共 **3 个布局项**，`layout_002` / `layout_003` 的 `parentLayoutId` 指向 `layout_001`，形成单层嵌套：

```json
[
  {
    "formId": "1234567890123456789",
    "layoutId": "layout_001",
    "parentLayoutId": "",
    "layoutType": "101",
    "layoutOrder": 1
  },
  {
    "formId": "1234567890123456789",
    "layoutId": "layout_002",
    "parentLayoutId": "layout_001",
    "layoutType": "102",
    "layoutOrder": 2
  },
  {
    "formId": "1234567890123456789",
    "layoutId": "layout_003",
    "parentLayoutId": "layout_001",
    "layoutType": "102",
    "layoutOrder": 3
  }
]
```

布局层级关系一目了然：

```
layout_001 (根)
 ├── layout_002
 └── layout_003
```

---

## 字段说明

### desForm.json

| 字段 | 示例值 | 说明 |
|---|---|---|
| `formId` | `1234567890123456789` | 表单唯一ID，**必填**，移植时的匹配键 |
| `formName` | `SampleForm` | 表单英文名 |
| `formAlias` | `样例表单` | 表单中文别名 |
| `useState` | `1` | 1=启用 |

### desFormControl.json

| 字段 | 示例值 | 说明 |
|---|---|---|
| `formId` | `1234567890123456789` | 所属表单ID |
| `formFieldId` | `ctrl_001` | 控件ID，移植时重新生成 |
| `layoutId` | `layout_001` | 布局ID，关联 desFormLayout |
| `formFieldDescribe` | `机构名称` | 表单项描述（表格"表单项"列） |
| `boundProperty` | `SampleForm.orgName` | 绑定属性（表格"绑定属性"列） |
| `generalDictionary` | `9876543210987654321` | 普通字典项ID（表格"字典项"列） |
| `treeShape` | `1122334455667788990` | 树形字典ID（表格"树形字典"列） |

### desFormLayout.json

| 字段 | 示例值 | 说明 |
|---|---|---|
| `formId` | `1234567890123456789` | 所属表单ID |
| `layoutId` | `layout_001` | 布局ID，移植时重新生成 |
| `parentLayoutId` | `layout_001` | 父布局ID，移植时按替换规则匹配 |

---

## 第一步：打包为 zip

使用 `zip_util.py` 将 `数据样例` 目录下的三个 JSON 打包：

```bash
# 打包（自动命名为 数据样例.zip）
python zip_util.py zip 数据样例

# 或指定输出名称
python zip_util.py zip 数据样例 -o 样例表单.zip
```

> 工具会自动只把目录下的文件打入 zip 根目录（扁平结构），不会创建多余文件夹。

生成 `数据样例.zip`（或 `样例表单.zip`）后即可用于后续演示。

---

## 演示：探查控件 → Markdown 表格

```bash
python dyFormMain.py          # 选择 1
# 或
python form_inspect.py        # 单独运行
```

输入 `数据样例/数据样例.zip`，输出如下：

```
| 序号 | 表单项 | 绑定属性 | 字典项 | 树形字典 |
|---|---|---|---|---|
| 1 | 机构名称 | SampleForm.orgName | - | - |
| 2 | 资产分类 | SampleForm.assetCategory | 9876543210987654321 | - |
| 3 | 业务分类 | SampleForm.bizCategory | - | （树形）1122334455667788990 |

共 3 条记录
```

- 第1行：普通文本控件，无字典无树形 → 两列均显示 `-`
- 第2行：下拉选择控件，有 `generalDictionary` → 字典项列显示 ID
- 第3行：树形选择控件，有 `treeShape` → 树形字典列显示 `（树形）ID`

---

## 演示：表单移植

假设有一个**旧表单 zip**（`formId = 1234567890123456789`）和**新表单 zip**（`formId = 9999999999999999999`），将旧表单的控件布局移植到新表单：

```bash
python dyFormMain.py          # 选择 2
# 或
python form_migrate.py        # 单独运行
```

移植过程（基于样例数据）：

```
1. 校验两个 zip 均为单表单 → 通过
2. 解压两个 zip
3. 提取 formId: 旧=1234567890123456789, 新=9999999999999999999
4. 构建替换规则（扫描 desFormLayout.json + desFormControl.json） → 7 条：

   formId:        1234567890123456789  →  9999999999999999999
   layout_001     →  1232026071517012001      (新生成的ID)
   layout_002     →  1232026071517012002      (新生成的ID)
   layout_003     →  1232026071517012003      (新生成的ID)
   ctrl_001       →  1232026071517012004      (新生成的ID)
   ctrl_002       →  1232026071517012005      (新生成的ID)
   ctrl_003       →  1232026071517012006      (新生成的ID)

5. 替换旧表单目录中的 desFormLayout.json 和 desFormControl.json
6. 覆盖到新表单目录
7. 重新打包为新 zip
```

注意：`layoutId` 和 `formFieldId` 会被移植脚本自动重新生成（基于当前时间戳 + 序号），无需手动指定。

---

## 演示：zip 命令行工具

所有演示均基于 `数据样例` 目录：

```bash
# 【打包】将数据样例目录下的 JSON 压为 zip
python zip_util.py zip 数据样例

# 【指定输出名称】
python zip_util.py zip 数据样例 -o 样例表单.zip

# 【解压】到指定目录
python zip_util.py unzip 数据样例.zip -d ./解压输出

# 【解压】到同名文件夹（默认）
python zip_util.py unzip 数据样例.zip

# 【查看帮助】
python zip_util.py unzip --help
python zip_util.py zip --help
```

完整的工作流示例：

```bash
# 1. 打包样例
python zip_util.py zip 数据样例 -o 样例表单.zip

# 2. 解压回来看结构（验证扁平格式）
python zip_util.py unzip 样例表单.zip -d ./tmp
ls ./tmp/
# 输出: desForm.json  desFormControl.json  desFormLayout.json
#        ↑ 文件直接出现，没有多余的文件夹包裹 ✓

# 3. 清理
rm -rf ./tmp
```

---

## 注意事项

- `desForm.json` 必须为**单元素列表**，多元素会被 `validate_single_form_zip` 直接拒绝（抛出 `ValueError`）
- zip 必须是**扁平结构**（文件直接在 zip 根目录），不能有子文件夹包裹
- 三个 JSON 中的 `formId` 需保持**一致**（表示同一表单）
- `layoutId` 和 `formFieldId` 会被移植脚本自动重新生成，样例中的占位值仅作参考
- 移植只改写 `target_files`（`desFormLayout.json` + `desFormControl.json`），其余文件不动
