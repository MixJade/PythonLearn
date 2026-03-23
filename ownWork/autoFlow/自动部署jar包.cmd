@echo off
chcp 65001 > nul
python "auto_deploy_jar.py" "cm_xxx_jar_config.json"
pause