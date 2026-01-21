# Ticketsystem

## Rask setup
- CMD: `setup.bat` (lag venv, installer) eller `setup.bat -run` for å starte

## Manuell ekstrem kjedelig og treig kjøring
1) Lag venv  
   `python -m venv venv`  

2) Installer Flask  
   `pip install -r requirements.txt`

3) Start server  
   `python app.py`

4) Logg inn  
   Brukernavn: `admin`  
   Passord: `1234`

Endre `USER` og `secret_key` i `app.py` om du vil ha andre verdier.
