# Ticketsystem (enkelt) (burde brukt bare .js :O )

Liten Flask-app som lar deg registrere brukere og tickets i MariaDB via PyMySQL. Lager en admin-bruker (`admin` / `1234`) automatisk hvis den mangler.

## Hva jeg tenkte
- Ville ha en superenkel ticket-løsning demo jeg kan kjøre lokalt.
- Alt skal være lett å endre: `.py`-fil + noen templates og statiske filer.
- Bruker MariaDB fordi jeg allerede har den kjørende.

## Hva jeg skal legge til
- Egen måte å bytte passord og generere ny `SECRET_KEY`.
- Bedre validering på felter (lengde, HTML escaping).
- Filopplasting for skjermbilder på tickets, kan være veldig nyttig for it folk så slipper de å bruke 1000 år på å vente på at kunden svarer.
- Enkel søk/filtrering i ticket-listen.

## Rask setup
- CMD: `./setup.bat` eller `setup.bat -run` for å kjøre serveren direkte.

## Database
Lag databasen i MariaDB:
```sql
CREATE DATABASE ticketsystem CHARACTER SET utf8mb4;
```
Standard tilkobling bruker:
- host: `localhost`
- port: `33096`
- db-navn: `ticketsystem`
- bruker: `root`
- passord: `badosbados`

Environment-variabler du kan override med:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `SECRET_KEY`


## Manuell setup (uten script) veldig treigt...
1) Lag venv: `python -m venv venv`
2) Aktiver venv: `venv\Scripts\activate.bat`
3) Installer deps: `pip install -r requirements.txt`
4) Start server: `python app.py`

Logg inn med `admin` / `1234`. Husk å endre `SECRET_KEY` og lage egen admin-bruker.



