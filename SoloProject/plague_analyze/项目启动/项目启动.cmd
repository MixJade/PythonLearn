@echo off
chcp 65001 >nul
cd ..\static\html
start 汇总网页.html
cd ..\..
python manage.py runserver localhost:8000
pause