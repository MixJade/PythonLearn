@echo off
chcp 65001 >nul
cd ../../mdUtil
python PandocMdToEpub.py
pause