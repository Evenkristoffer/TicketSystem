# TicketSystem - enkel dokumentasjon

## Hva er dette?
En liten Flask-app med MariaDB. Funksjoner:
- Registrering med rolle (admin/support/ansatt)
- Innlogging/utlogging
- Dashboard med oppretting og visning av tickets

## Krav for aa kjoere
- Python 3.10+ (med pip)
- MariaDB som kjører lokalt (eller tilgjengelig host)
- Databasenavn `ticketsystem` (kan overstyres med DB_NAME)

## Setup raskt
- CMD: `setup.bat` eller `setup.bat -run` (lager venv, installerer, starter)
- PowerShell: `.\setup.ps1` eller `.\setup.ps1 -Run`

## Manuell setup (kort)
1) Lag venv: `python -m venv venv`
2) Aktiver: `venv\Scripts\activate` (tilpass for PS/CMD)
3) Installer: `pip install -r requirements.txt`
4) Start: `python app.py`

## Miljo-variabler (valgfrie)
`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `SECRET_KEY`

## Database
Opprett DB hvis den ikke finnes:
```sql
CREATE DATABASE ticketsystem CHARACTER SET utf8mb4;
```
Appen lager tabeller og seed’er en admin-bruker (`admin`/`1234`) hvis den mangler.

## Ruter (enkelt)
- `/` (GET/POST): login
- `/register` (GET/POST): registrer ny bruker med rolle
- `/dashboard` (GET/POST): liste og opprett tickets (auth kreves)
- `/logout`: logg ut

## Data-modell
- `users`: id, brukernavn, passord_hash, rolle (`admin`, `support`, `ansatt`)
- `tickets`: id, bruker_id (FK), tittel, beskrivelse, status (`apen`, `under arbeid`, `lukket`)

## Videre arbeid (enkle ideer)
- Legg til status-endring og filtrering per rolle
- Legg til "ta ticket" for support/admin
- Lag en enkel API (JSON) for tickets
