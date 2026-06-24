@echo off
chcp 65001 >nul
cd ../../dataGen
python GenGitPatches.py
pause