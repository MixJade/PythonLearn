@echo off
chcp 65001 >nul
python ../GetPrjGitRecords.py -a 样例配置.json -b 项目管理 -s _
pause