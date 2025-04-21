# coding=utf-8
# @Time    : 2025/4/21 20:59
# @Software: PyCharm
import json
import os

import requests

# noinspection SpellCheckingInspection
ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/86.0.4240.198 Safari/537.36"'}
# 保存路径(斜线结尾)
dir_path = r"../../outputFile/creepLrc/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)


def get_lyrics(song_id, song_name):
    url = f"https://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=-1"
    try:
        response = requests.get(url, headers=ua)
        response.raise_for_status()
        data = response.json()
        if 'lrc' in data and 'lyric' in data['lrc']:
            # 4. 保存数据
            with open(dir_path + song_name + '.lrc', 'w', encoding='utf-8') as file:
                file.write(data['lrc']['lyric'])
            print(f"歌词已写入{dir_path}{song_name}.lrc")
        else:
            return "未找到歌词"
    except requests.RequestException as e:
        print(f"请求出错: {e}")
    except (KeyError, json.JSONDecodeError):
        print("解析数据出错")
    return None


if __name__ == "__main__":
    song_id_1 = "2694678809"  # 请替换为实际的歌曲 ID
    song_name_1 = '儒风诉骨'
    # 这里的歌曲自己下载,只下歌词
    get_lyrics(song_id_1, song_name_1)
