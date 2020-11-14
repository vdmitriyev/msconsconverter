@echo off
REM Remove comment in case virtualenv is used
REM call ..\.venv\Scripts\activate.bat
echo "Check 'logfile-{0}.log' file for processing details"
python msconsconverter.py '../data/' 'MSCONS_TL_SAMPLE01.txt,MSCONS_TL_SAMPLE02.txt' --verbose
pause