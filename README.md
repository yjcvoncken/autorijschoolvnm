# Autorijschool VNM – Django

## Installeren en starten

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_vnm
python manage.py createsuperuser
python manage.py runserver
```

Open de website op `http://127.0.0.1:8000/` en het beheer op
`http://127.0.0.1:8000/beheer/` (of `/admin/`).

Via het beheer kunnen website-instellingen, pakketten, galerijfoto's en
contactaanvragen worden beheerd.

## Formulieren per e-mail ontvangen

Vul onder **Beheer → Contactgegevens → Ontvangstadres formulieren** het
Gmail-adres in waarop aanvragen moeten aankomen. Voeg daarna op Railway deze
variabelen toe:

```text
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=true
EMAIL_HOST_USER=jouwaccount@gmail.com
EMAIL_HOST_PASSWORD=je_16_cijferige_google_appwachtwoord
DEFAULT_FROM_EMAIL=jouwaccount@gmail.com
```

Gebruik voor `EMAIL_HOST_PASSWORD` een Google-appwachtwoord, niet het gewone
Gmail-wachtwoord. Lokaal, zonder SMTP-variabelen, wordt de e-mail alleen in de
terminal afgedrukt. De aanvraag wordt altijd ook in Django Admin opgeslagen.

Voor productie moeten `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, e-mail en de
opslag van statische/media-bestanden via omgevingsvariabelen en hosting worden
geconfigureerd.

Gebruik buiten Railway `ALLOWED_HOSTS` en `CSRF_TRUSTED_ORIGINS` als
komma-gescheiden variabelen, bijvoorbeeld:

```text
DJANGO_DEBUG=false
ALLOWED_HOSTS=autorijschoolvnm.nl,www.autorijschoolvnm.nl
CSRF_TRUSTED_ORIGINS=https://autorijschoolvnm.nl,https://www.autorijschoolvnm.nl
```

Op Railway wordt `RAILWAY_PUBLIC_DOMAIN` automatisch aan beide lijsten
toegevoegd, zodat inloggen en opslaan in het beheer via HTTPS blijft werken.

## Railway deployment

Koppel deze repository als service in Railway en voeg een PostgreSQL-service
toe. Railway levert `DATABASE_URL` dan automatisch aan Django. De `Procfile`
voert bij elke deployment migraties en `collectstatic` uit en start Gunicorn.

Stel minimaal deze variabelen in:

```text
DJANGO_DEBUG=false
SECRET_KEY=een-lange-willekeurige-geheime-waarde
ALLOWED_HOSTS=autorijschoolvnm.nl,www.autorijschoolvnm.nl
CSRF_TRUSTED_ORIGINS=https://autorijschoolvnm.nl,https://www.autorijschoolvnm.nl
```

Geüploade galerijfoto's hebben voor blijvende opslag een Railway Volume nodig.
Koppel dit volume aan `/app/media` en stel `MEDIA_ROOT=/app/media` in. De foto's
die al in deze repository staan, worden ook zonder volume meegeleverd.

Maak na de eerste deployment een beheerder via de Railway Shell:

```bash
python manage.py createsuperuser
```
