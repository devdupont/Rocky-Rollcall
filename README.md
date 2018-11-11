# Rocky-Rollcall

[![Requirements Status](https://requires.io/github/flyinactor91/Rocky-Rollcall/requirements.svg?branch=master)](https://requires.io/github/flyinactor91/Rocky-Rollcall/requirements/?branch=master)

Directory for Rocky Horror Picture Show casts

## Setup

First we should install the app requirements and copy the env file. I recommend always installing into a virtual environment.

```bash
pip install -r requirements.txt
cp .env.sample .env
```

The app uses a Postgres backend. To run locally, you'll need to create a rocky database and owner.

```sql
CREATE USER rocky;
CREATE DATABASE rocky OWNER rocky;
```

You'll also need to enable some extensions.

```sql
CREATE EXTENSION pg_trgm;
```

Now that the database is set up, run the app migrations to deploy all of the models to the database.

```bash
./manage.py migrate
```

Finally, the server should be able to start on localhost:8000

```bash
./manage.py runserver
```

## Deploy

```bash
git push heroku master
```