# coding=utf-8
# @Time    : 2026/4/2 11:01
# @Software: PyCharm
from PIL import Image
import os
from datetime import datetime


def merge_images_vertically(images):
    """
    垂直拼接图片（上下拼接）
    :param images: 图片对象列表
    :return: 拼接后的图片对象
    """
    # 计算总高度和最大宽度
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)
    # 创建新画布
    merged_image = Image.new('RGB', (max_width, total_height))
    # 依次粘贴图片
    current_y = 0
    for img in images:
        # 居中粘贴（宽度不足则居中）
        x = (max_width - img.width) // 2
        merged_image.paste(img, (x, current_y))
        current_y += img.height
    return merged_image


def main():
    image_paths = []  # 存储待拼接的图片路径
    first_dir = None  # 第一张图片的文件夹（保存路径）
    print("===== 图片拼接工具 =====")
    print("规则：输入图片路径 → 0取消 / 1确认 / 继续输入路径追加")
    print("-" * 30)
    while True:
        # 输入图片路径
        path = input("请输入图片路径：").strip()
        # 校验路径是否为空
        if not path:
            print("路径不能为空，请重新输入！")
            continue
        # 判断输入是否为数字指令
        if path in ["0", "1"]:
            # 取消拼接
            if path == "0":
                print("已取消拼接，程序退出！")
                return
            # 确认拼接
            if path == "1":
                if len(image_paths) < 2:
                    print("错误：至少需要2张图片才能拼接！")
                    continue
                break
        # 正常图片路径 → 校验并添加
        try:
            with Image.open(path) as img:
                img.verify()  # 校验是否为有效图片
        except Exception as e:
            print(f"无效图片路径：{e}，请重新输入！")
            continue
        # 添加到列表
        image_paths.append(path)
        print(f" 已追加图片，当前共 {len(image_paths)} 张")
        # 记录第一张图片的文件夹
        if first_dir is None:
            first_dir = os.path.dirname(os.path.abspath(path))
    # ===================== 开始拼接 =====================
    print("\n正在拼接图片，请稍候...")
    # 打开所有图片
    images = [Image.open(p) for p in image_paths]
    # 执行拼接
    result_img = merge_images_vertically(images)
    # 生成文件名：图片拼接+月日时分秒
    time_str = datetime.now().strftime("%m%d%H%M%S")
    filename = f"图片拼接{time_str}.jpg"
    save_path = os.path.join(first_dir, filename)
    # 保存图片
    result_img.save(save_path)
    # 关闭图片对象
    for img in images:
        img.close()
    result_img.close()
    print(f"\n 拼接完成！")
    print(f"保存路径：{save_path}")


if __name__ == "__main__":
    main()
