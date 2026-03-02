@echo off
:: 1. Cria o ambiente virtual se ele não existir
if not exist "venv" (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: 2. Ativa o ambiente e instala as dependências
echo Atualizando dependencias...

call venv\Scripts\activate
pip install -r requirements.txt --quiet

:: 3. Roda o seu script
echo Iniciando o AutoClicker...
python auto_clicker.py

:: 4. Mantém a janela aberta se o script fechar
pause