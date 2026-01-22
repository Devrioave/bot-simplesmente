@echo off
title Simplesmente Bot - Autostart
echo ==========================================
echo   A iniciar FastAPI e Localtunnel...
echo ==========================================

:: 1. Iniciar o FastAPI numa nova janela
start cmd /k "call .venv\Scripts\activate && uvicorn app.main:app --reload"

:: 2. Aguardar 3 segundos para o servidor subir
timeout /t 3 /nobreak > nul

:: 3. Iniciar o Localtunnel noutra janela
start cmd /k "npx localtunnel --port 8000 --subdomain bot-simplesmente"

echo.
echo [OK] Servidores em execução em janelas separadas.
echo [!] Lembre-se de confirmar o bypass no link do Localtunnel.
echo ==========================================
pause