#!/bin/bash  

pyinstaller --onefile \       
    --icon=iconformatter.ico \        
    --add-data "src/BG3_icon_formatter.py:." \
    src/BG3_icon_formatter.py