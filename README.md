# Ticketsystem (veldig enkel)

Lagres brukere og tickets i MariaDB via PyMySQL. admin (admin/1234) om den ikke finnes.

## Rask setup
- CMD: `./setup.bat` eller `setup.bat -run` for å starte

## Database
Lag databasen i MariaDB:
```sql
CREATE DATABASE ticketsystem CHARACTER SET utf8mb4;
```
Standard tilkobling bruker:
- host: `localhost`
- port: `3306`
- db-navn: `ticketsystem`
- bruker: `root`
- passord: insert når det er lagd

Override med environment-variables hvis du trenger:
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`

## Manuell ekstrem kjedelig og treig kjøring
1) Lag venv  
   `python -m venv venv`

2) Activate venv  
   CMD: `venv\Scripts\activate.bat`

3) Installer dependencies
   `pip install -r requirements.txt`

4) Start server  
   `python app.py`

Logg inn med `admin` / `1234`. Endre `SECRET_KEY` og opprett bruker i register.html.
