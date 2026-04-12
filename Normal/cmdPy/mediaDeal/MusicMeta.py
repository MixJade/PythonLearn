# coding=utf-8
# @Time    : 2026/4/12 21:25
# @Software: PyCharm
import json
import os
import subprocess

"""
音乐元数据的读取、重写
"""


def get_audio_info_with_ffmpeg(file_path):
    """使用ffprobe读取音频元数据"""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_format",
        file_path
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        info = json.loads(result.stdout)
        tags = info.get("format", {}).get("tags", {})

        title = tags.get("title") or tags.get("Title") or "未知歌曲"
        artist = tags.get("artist") or tags.get("Artist") or "未知歌手"
        album = tags.get("album") or tags.get("Album") or "未知专辑"

        return title, artist, album

    except Exception as e:
        return f"读取失败：{str(e)}", "", ""


def write_audio_metadata_with_ffmpeg(input_path, title, artist, album):
    """使用ffmpeg写入元数据，生成新文件，不覆盖原文件"""
    dir_name = os.path.dirname(input_path)
    file_name = os.path.basename(input_path)
    name, ext = os.path.splitext(file_name)

    # 1. 先生成临时文件
    temp_path = os.path.join(dir_name, f"~temp_{name}{ext}")

    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-c", "copy",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album={album}",
        "-y",
        temp_path  # 先写入临时文件
    ]

    try:
        # 执行写入
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8"
        )
        # 检查 ffmpeg 是否真的成功
        if result.returncode != 0:
            print(f"\n ffmpeg 写入失败！错误信息：")
            print(result.stderr)
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return
        # 只有成功了才替换
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            os.replace(temp_path, input_path)
            print(f"\n 成功覆盖原文件！")
            print(f"文件路径：{input_path}")
        else:
            print("\n 写入失败：生成的文件为空！")
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception as e:
        print(f"\n 写入失败：{str(e)}")
        # 失败了就删掉临时文件
        if os.path.exists(temp_path):
            os.remove(temp_path)


def input_with_default(prompt, default):
    """带默认值的输入函数
    """
    default_txt = ""
    if default != "":
        default_txt = f" [默认：{default}]"
    user_input = input(f"{prompt}{default_txt}：").strip()
    return user_input if user_input else default


if __name__ == "__main__":
    print("===== ffmpeg 音频标签 读取+写入工具 =====")
    last_artist, last_album = "", ""

    while True:
        # 1. 输入音频路径
        audio_path = input("请拖入音频文件：").strip().strip('"')

        if not os.path.exists(audio_path):
            print("文件不存在！")
            exit()

        # 2. 读取并显示原有信息
        print("\n正在读取现有标签信息...")
        old_title, old_artist, old_album = get_audio_info_with_ffmpeg(audio_path)
        print("=== 当前标签信息 ===")
        print(f"歌曲名：{old_title}")
        print(f"歌手：{old_artist}")
        print(f"专辑：{old_album}")

        # 3. 自动获取新标题（文件名无后缀）
        file_name_without_ext = os.path.splitext(os.path.basename(audio_path))[0]
        print(f"\n 设置新歌曲名：{file_name_without_ext}")

        # 4. 手动输入歌手、专辑
        new_artist = input_with_default("请输入【歌手】", last_artist)
        new_album = input_with_default("请输入【专辑】", last_album)
        last_artist, last_album = new_artist, new_album

        # 5. 确认是否写入
        print("\n=== 即将写入的信息 ===")
        print(f"歌曲名：{file_name_without_ext}")
        print(f"歌手：{new_artist}")
        print(f"专辑：{new_album}")

        choice = input("\n确认写入？1=是  0=否：").strip()

        if choice == "1":
            write_audio_metadata_with_ffmpeg(
                audio_path,
                file_name_without_ext,
                new_artist,
                new_album
            )
        else:
            print("\n已取消写入～")
