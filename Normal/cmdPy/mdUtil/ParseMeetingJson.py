# coding=utf-8
# @Time    : 2026/4/16 16:43
# @Software: PyCharm
import json
import os
from collections import OrderedDict
from pathlib import Path

"""
腾讯会议转写JSON解析工具
功能：解析会议转写JSON文件，提取发言人、发言内容，并去重整理

JSON来源：
    1. 腾讯会议的转写链接，通过网页打开，
    2. 然后F12查看调取的`detail?c_app_id=`接口（可能有多个，将对话列表滑动到最下面可以全部加载）
"""


def parse_meeting_json(file_path: str) -> list[dict]:
    """解析腾讯会议转写JSON文件

    :param file_path: JSON文件路径
    :return: 去重后的对话列表，每项包含发言人、发言内容、时间信息
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # 用于去重的OrderedDict，按sid顺序保留
    unique_dialogues = OrderedDict()
    # 获取paragraphs
    paragraphs = data.get('minutes', {}).get('paragraphs', [])
    for paragraph in paragraphs:
        # 获取发言人信息
        speaker_info = paragraph.get('speaker', {})
        speaker_name = speaker_info.get('user_name', '未知发言人')
        paragraph_start = paragraph.get('start_time', 0)
        paragraph_end = paragraph.get('end_time', 0)
        # 解析每句话
        sentences = paragraph.get('sentences', [])
        for sentence in sentences:
            sid = sentence.get('sid')
            if sid is None:
                continue
            # 获取发言内容
            words = sentence.get('words', [])
            content = ''
            for word in words:
                text = word.get('text', '').strip()
                if text:
                    content += text
            if content and sid not in unique_dialogues:
                unique_dialogues[sid] = {
                    'sid': sid,
                    'speaker': speaker_name,
                    'content': content,
                    'start_time': sentence.get('start_time', paragraph_start),
                    'end_time': sentence.get('end_time', paragraph_end),
                    'pid': paragraph.get('pid', '')
                }
    return list(unique_dialogues.values())


def format_time_readable(ms: int) -> str:
    """将毫秒转换为易读的 MM:SS 格式"""
    seconds = ms // 1000
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


def export_to_markdown(dialogues: list[dict], output_path: str):
    """导出为Markdown格式"""
    current_speaker = None

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# 会议转写记录\n\n")
        f.write("> 自动生成时间: " + __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        f.write("---\n\n")

        for dialogue in dialogues:
            speaker = dialogue['speaker']
            content = dialogue['content']
            start_time = dialogue['start_time']

            # 发言人变化时，打印分隔线
            if speaker != current_speaker:
                f.write("\n## " + speaker + "\n\n")
                current_speaker = speaker

            # 格式化时间
            time_str = format_time_readable(start_time)
            f.write(f"**[{time_str}]** {content}\n\n")


def export_summary(dialogues: list[dict]) -> dict:
    """生成对话统计摘要"""
    # 统计每个发言人的发言次数和总字数
    speaker_stats = {}
    for d in dialogues:
        speaker = d['speaker']
        if speaker not in speaker_stats:
            speaker_stats[speaker] = {'count': 0, 'chars': 0}
        speaker_stats[speaker]['count'] += 1
        speaker_stats[speaker]['chars'] += len(d['content'])

    return {
        'total_turns': len(dialogues),
        'total_chars': sum(s['chars'] for s in speaker_stats.values()),
        'speaker_stats': speaker_stats
    }


def print_summary(summary: dict):
    """打印统计摘要"""
    print("\n" + "=" * 60)
    print("[Stats] 会议转写统计")
    print("=" * 60)
    print(f"总发言轮次: {summary['total_turns']}")
    print(f"总字符数: {summary['total_chars']}")
    print("\n各发言人统计:")
    print("-" * 40)
    for speaker, stats in summary['speaker_stats'].items():
        print(f"  {speaker}: {stats['count']} 轮, {stats['chars']} 字")


def main():
    """主函数：循环输入JSON文件路径"""
    print("=" * 60)
    print("[Meeting Parser] 腾讯会议转写JSON解析工具")
    print("=" * 60)
    print("JSON来源：")
    print("    1. 腾讯会议的转写链接，通过网页打开")
    print("    2. F12查看`detail?c_app_id=`接口（可能多个，将对话列表滑动到最下面以全部加载）")
    print("=" * 60)
    print("功能说明:")
    print("  1. 循环输入JSON文件路径")
    print("  2. 输入回车确认，开始解析")
    print("  3. 自动去重(sid)并提取发言人、发言内容")
    print("=" * 60)
    all_dialogues = []
    file_list = []

    while True:
        print("\n" + "-" * 40)
        print("请输入JSON文件路径（直接回车结束输入）:")
        print("> ", end="")

        # ── 去掉拖入文件时系统自动添加的引号
        path = input().strip().strip('"').strip("'")
        # 空输入表示结束
        if not path:
            if not file_list:
                print("\n未输入任何文件，程序退出。")
                return
            break
        # 检查文件是否存在
        if not os.path.exists(path):
            print(f"[WARN] 文件不存在: {path}")
            continue
        # 检查是否为JSON文件
        if not path.lower().endswith('.json'):
            print(f"[WARN] 请输入JSON文件: {path}")
            continue
        file_list.append(path)
        print(f"[OK] 已添加: {path}")

    # 确认开始解析
    print("\n" + "-" * 40)
    print(f"已添加 {len(file_list)} 个文件:")
    for f in file_list:
        print(f"  - {f}")
    # 解析所有文件
    print("\n正在解析文件...")

    for file_path in file_list:
        try:
            dialogues = parse_meeting_json(file_path)
            all_dialogues.extend(dialogues)
            print(f"[OK] 解析完成: {Path(file_path).name} ({len(dialogues)} 条发言)")
        except Exception as e:
            print(f"[FAIL] 解析失败: {Path(file_path).name} - {str(e)}")
    if not all_dialogues:
        print("\n[WARN] 没有解析到任何对话内容")
        return

    # 去重（按sid）
    unique_dialogues = []
    seen_sids = set()
    for d in all_dialogues:
        if d['sid'] not in seen_sids:
            seen_sids.add(d['sid'])
            unique_dialogues.append(d)
    # 按时间排序
    unique_dialogues.sort(key=lambda x: x['start_time'])

    print(f"\n去重后共 {len(unique_dialogues)} 条发言")

    # 生成统计摘要
    summary = export_summary(unique_dialogues)
    print_summary(summary)
    # 自动生成输出文件名
    first_file = Path(file_list[0])
    base_name = first_file.stem
    output_dir = first_file.parent
    md_path = output_dir / f"{base_name}_转写记录.md"
    export_to_markdown(unique_dialogues, str(md_path))
    print(f"[OK] 已导出: {md_path}")
    print("\n[Done] 处理完成！")


if __name__ == "__main__":
    main()
