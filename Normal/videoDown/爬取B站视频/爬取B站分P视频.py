# coding=utf-8
# @Time    : 2025-04-03 21:51
# @Software: PyCharm

import json
import os
import re
import subprocess

import requests

"""下载某分P的所有视频（两阶段）
第一阶段：遍历所有分P，解析出视频/音频地址，写成 json 清单
第二阶段：只读 json 清单去下载、合并

目录下已存在 video_links.json 时，视为已经抓取过，自动跳过第一阶段；
想强制重新抓取（例如链接过期、改了分P范围），删掉该 json 文件再运行即可。
"""

# ==============================[配置区]==============================
# 选择一个视频的url(如果是分p视频则带上最后的p参数，但不要放“p=”后的那个数字)
url = r'https://www.bilibili.com/video/BV1YLoYYcEyx/?spm_id_from=3333&p='
# 开始和结束分P
begin_p, en_p = 2, 32

# 设置请求头
# 如果出现下载不了的情况，可以试试带上Cookie（下载更高清晰度也需要登录）
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 "
                  "Safari/537.36 Edg/118.0.2088.76",
    "Referer": "https://www.bilibili.com/",  # 设置防盗链
    # "cookie": "xxx",
}

# 保存路径(非斜杠结尾)
dir_path = r"../../outputFile/creepB2P"
out_dir_path = os.path.join(dir_path, "output")
print("保存路径", dir_path)
# 链接清单文件（第一步产出、第二步消费）
json_path = os.path.join(dir_path, "video_links.json")

if not os.path.exists(dir_path):
    os.makedirs(dir_path)
if not os.path.exists(out_dir_path):
    os.makedirs(out_dir_path)

# 匹配页面中的 playinfo 数据
playinfo_pattern = re.compile(r'window.__playinfo__=(.*?)</script>', re.S)


# ==============================[第一步：抓取全部分P的下载链接]==============================
def parse_one_p(it_p):
    """解析第 i P，返回 {'p':i, 'video_url':..., 'audio_url':...}；失败返回 None"""
    resp = requests.get(url=f"{url}{it_p}", headers=header, timeout=30)
    html_data = playinfo_pattern.findall(resp.text)[0]  # 从列表转换为字符串
    json_data = json.loads(html_data)

    # video 和 audio 分别是视频流和音频流（dash 格式），因此下载后还需要合并
    videos = json_data['data']['dash']['video']  # 这里得到的是一个列表，只取第一条
    audios = json_data['data']['dash']['audio']
    return {
        "p": it_p,
        "video_url": videos[0]['baseUrl'],  # 视频地址
        "audio_url": audios[0]['baseUrl'],  # 音频地址
    }


def fetch_all_links(begin1_p, en1_p):
    """遍历所有分P，把所有下载链接汇总写入 json 文件"""
    tasks1 = []
    for it_p in range(begin1_p, en1_p + 1):
        try:
            task1 = parse_one_p(it_p)
            tasks1.append(task1)
            print(f"[解析成功] 第{it_p}P")
            print("  视频地址: " + task1['video_url'])
            print("  音频地址: " + task1['audio_url'])
        except Exception as e:
            # 单P失败不影响整体，记录下来跳过即可
            print(f"[解析失败] 第{it_p}P -> {type(e).__name__}: {e}")

    with open(json_path, mode='w', encoding='utf-8') as fw:
        json.dump(tasks1, fw, ensure_ascii=False, indent=2)
    print(f"\n[链接清单] 共 {len(tasks1)} 条，已写入: {json_path}")


# 已有清单就跳过抓取（清单存在但内容为空/损坏时仍然重抓）
if os.path.exists(json_path) and os.path.getsize(json_path) > 2:
    print(f"[跳过抓取] 已存在链接清单，直接进入下载: {json_path}")
    print("           如需重新抓取链接，请先删除该文件")
else:
    fetch_all_links(begin_p, en_p)


# ==============================[第二步：按 json 清单下载]==============================
def download_file(file_url, save_path):
    """流式下载单个文件，已存在且非空则跳过"""
    if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
        print(f"  已存在，跳过: {save_path}")
        return
    print("  下载: " + file_url)
    with requests.get(url=file_url, headers=header, stream=True, timeout=60) as resp:
        resp.raise_for_status()
        with open(save_path, mode='wb') as fw:
            for chunk in resp.iter_content(chunk_size=1024 * 256):
                if chunk:
                    fw.write(chunk)


# 读取清单
with open(json_path, mode='r', encoding='utf-8') as f:
    tasks = json.load(f)

print(f"[开始下载] 清单中共 {len(tasks)} 个分P")
for task in tasks:
    i = task['p']
    print(f"========================[下载第{i}P]================================")
    download_file(task['video_url'], f'{dir_path}/test{i}.mp4')
    download_file(task['audio_url'], f'{dir_path}/test{i}.mp3')

print("=============================[爬取完成]=======================================")

# ==============================[第三步：合并音视频 需要模块ffmpeg]==============================
for task in tasks:
    i = task['p']
    print(f"------------------------[合并第{i}P]------------------------")
    command = [
        "ffmpeg", "-y",
        "-i", f'{dir_path}/test{i}.mp4',
        "-i", f'{dir_path}/test{i}.mp3',
        "-acodec", "copy", "-vcodec", "copy",
        f'{out_dir_path}/testout{i}.mp4',
    ]
    # -y 覆盖旧文件，避免 ffmpeg 等待交互输入导致卡住
    subprocess.run(command)

print("=============================[全部完成]=======================================")
