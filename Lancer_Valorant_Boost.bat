@echo off
:: Vérifie si on est déjà admin
net session >nul 2>&1
if %errorlevel% == 0 (
    goto :run
) else (
    goto :elevate
)

:elevate
:: Demande les droits admin via PowerShell
powershell -Command "Start-Process '%~f0' -Verb RunAs"
exit

:run
:: Lance le script Python
cd /d "%~dp0"
python valorant_priority_boost.py
pause
