# Cmd隐藏黑框

> 2024年5月26日00:29:13

* 首先加上如下代码

```bash
@echo off
if "%1"=="h" goto begin
start mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
::以下为正常批处理命令，不可含有pause set/p等交互命令
```

* 然后将当前的cmd文件拉一个快捷方式出来
* 对该快捷方式设置【运行方式】-【最小化】