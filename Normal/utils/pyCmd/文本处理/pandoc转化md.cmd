@echo off
chcp 65001 >nul
cd ../../mdUtil
python pandoc转化md.py
pause