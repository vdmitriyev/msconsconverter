@echo off
cd ..
setlocal
:PROMPT
SET AREYOUSURE=N
SET /P AREYOUSURE=Do you want to create new virtual environment (Y/[N])?
IF /I "%AREYOUSURE%" NEQ "Y" GOTO END

SET PATH=C:\Compilers\Python312\Scripts\;C:\Compilers\Python312\;%PATH%
python -m venv .venv
call .\.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install uv
uv pip install -r requirements-prod.txt
uv pip install -r requirements-dev.txt

:END
endlocal
