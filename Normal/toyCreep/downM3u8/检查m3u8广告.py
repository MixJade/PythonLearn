# coding=utf-8
# @Time    : 2024/10/2 15:12
# @Software: PyCharm

m3u8_file_path = "../../outputFile/downM3u8/swbj/index.m3u8"
# 读取文件所有的行
with open(m3u8_file_path, 'r') as ts_f:
    lines = ts_f.readlines()
# 存储'#EXTINF'开头行的下一行
result = []
for i in range(len(lines)):
    if lines[i].startswith('#EXT-X-DISCONTINUITY'):
        if i + 7 > len(lines):
            continue
        # 将每个播放列表开头的ts文件名称，以及前三个ts文件的时长放入
        result.append((
            lines[i + 1].strip(),  # 当前文件时长
            lines[i + 3].strip(),  # 下1文件的时长
            lines[i + 5].strip(),  # 下2文件的时长
            lines[i + 7].strip(),  # 下3文件的时长
            lines[i + 2].strip(),  # ts文件名
        ))  # 使用strip()移除末尾的换行符
# 开始校验是否有重复列表
dicts = {}
for item in result:
    key = item[:4]  # 只考虑元组的前4个元素
    if key in dicts:
        dicts[key].append(item)
    else:
        dicts[key] = [item]

# 获取重复播放列表的开头ts名称列表
dup_ts_names_list = [value for value in dicts.values() if len(value) > 1]
print(f"重复的播放列表有{len(dup_ts_names_list)}组")
# 输出文件名
i = 1
for dup_ts_names in dup_ts_names_list:
    print(f"【疑似广告{i}】 ({dup_ts_names[0][0].replace('#EXTINF:', '')})")
    i += 1
    for dup_ts_name in dup_ts_names:
        print(dup_ts_name[-1])  # 输出文件名
