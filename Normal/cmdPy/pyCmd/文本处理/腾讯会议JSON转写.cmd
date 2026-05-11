@echo off
chcp 65001 > nul
cd ../../mdUtil
python ParseMeetingJson.py
pause