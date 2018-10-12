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
./manage.py migrate --settings=rocky.local_settings
./manage.py runserver --settings=rocky.local_settings
```

## Deploy

```bash
git push heroku master
```