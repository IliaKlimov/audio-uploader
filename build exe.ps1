pyinstaller -w -i "favicon.ico" -y --name="speechloader" main.py  --hidden-import settings
copy pids.txt dist\speechloader\pids.txt
copy settings.txt dist\speechloader\settings.txt
copy favicon.png dist\speechloader\favicon.png
ii dist\speechloader\
TIMEOUT 10