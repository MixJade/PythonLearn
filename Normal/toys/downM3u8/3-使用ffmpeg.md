# 3-使用ffmpeg

> 2024-08-24 00:00:36

## 一、ffmpeg命令

- 解密并转换文件夹下的m3u8为xxx.mp4

```shell
ffmpeg -allowed_extensions ALL -i index.m3u8 -c copy xxx.mp4
```

## 二、ffmpeg下载与配置

* 官网下载页面：[Download Ffmpeg](https://ffmpeg.org/download.html)
* 我推荐的win下载界面：[win下载Ffmpeg](https://www.gyan.dev/ffmpeg/builds/)
* 下载教程：[下载教程](https://blog.csdn.net/m0_47449768/article/details/130102406)

- 进入我推荐的下载界面下载第一个绿框里面的`ffmpeg-git-essentials.7z`
- 解压下载的包，找到里面的`bin`目录，添加到环境变量`path`中
- 然后运行`ffmpeg –version`查看是否安装成功