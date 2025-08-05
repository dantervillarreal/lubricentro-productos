@echo off
cd /d %~dp0
echo Activando entorno virtual...
python -m venv venv
call venv\Scripts\activate
echo Instalando dependencias...
pip install -r requirements.txt
echo Iniciando servidor Flask...
python app.py
pause
