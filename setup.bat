@echo off
color a
title Ticket System Setup Script | TechSupport AS | Created in Norway
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python app.py
