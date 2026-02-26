@echo off
python -m venv venv
pip install -r requirements.txt
python auto_key.py
pause