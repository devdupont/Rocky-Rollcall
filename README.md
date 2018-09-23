# Rocky-Rollcall
API listing Rocky Horror casts

## Setup

```bash
psql
create user rocky;
create database rocky owner rocky;
```

## Develop

```bash
python manage.py migrate --settings=rocky.local_settings
python manage.py runserver --settings=rocky.local_settings
```

## Deploy

```bash
git push heroku master
```