# learn-django
A repo for exploring the Django framework

## Increment 1: a tiny books app

This repo now contains a minimal Django project named `config`, one Django app
named `books`, and a Vite/Vue frontend in `frontend`.

The important files are:

- `manage.py`: command-line entry point for Django tasks.
- `config/settings.py`: project configuration, including installed apps and database settings.
- `config/urls.py`: URL routing for the whole project.
- `books/models.py`: database models for the books app.
- `books/admin.py`: Django admin configuration for book records.
- `books/migrations/0001_initial.py`: generated database change for the first `Book` table.
- `frontend/src/App.vue`: Vue application shell.
- `frontend/src/components/`: Vue components for the home page, books page, and navigation.

## First-time setup

Create the Python virtual environment and install backend dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

## Start and stop

Start PostgreSQL, Django, and Vite:

```bash
./server.sh start
```

Then open:

```text
http://127.0.0.1:5173/
```

The Vite frontend links to the books page, Django admin, and the books API.

Stop PostgreSQL, Django, and Vite:

```bash
./server.sh stop
```

The start command does four things:

- starts PostgreSQL with Docker Compose
- applies any pending Django migrations
- starts Django on `127.0.0.1:8000`
- starts Vite on `127.0.0.1:5173`

Django logs go to `.django.log`, and Vite logs go to `.vite.log`. The script
stores process IDs in `.django.pid` and `.vite.pid` so it can stop the same
processes later.

## Admin login

After starting the server, visit:

```text
http://127.0.0.1:8000/admin/
```

Local admin credentials:

```text
username: admin
password: LocalTest123!
```

## Books page

The custom books page is:

```text
http://127.0.0.1:5173/books
```

That page is a Vue component. It fetches book data from Django here:

```text
http://127.0.0.1:8000/api/books/
```

The flow is:

```text
Vue page -> Django JSON view -> Book model -> PostgreSQL
```

During development, Vite proxies `/api` requests to Django, so the Vue code can
call `/api/books/` without hard-coding the backend host.

## What we built

The `Book` model has three fields:

- `title`: short text, stored as a `varchar` column.
- `author`: short text, stored as a `varchar` column.
- `published_year`: positive integer, stored as an integer column.

When you run:

```bash
python manage.py makemigrations books
```

Django compares your model code to the existing migrations and creates a new
migration file if the model changed.

When you run:

```bash
python manage.py migrate
```

Django applies unapplied migrations to the PostgreSQL database.

## PostgreSQL settings

Django connects to PostgreSQL by default.

In production, set `DATABASE_URL` to the database connection URL from your host.
Railway's PostgreSQL service provides this value.

For local development, if you do not provide `DATABASE_URL`, Django uses these
defaults:

- database: `learn_django`
- user: `postgres`
- password: `postgres`
- host: `localhost`
- port: `5432`

You can override them when running Django:

```bash
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/learn_django \
python manage.py migrate
```

Or override the individual local settings:

```bash
POSTGRES_DB=learn_django \
POSTGRES_USER=postgres \
POSTGRES_PASSWORD=postgres \
POSTGRES_HOST=localhost \
POSTGRES_PORT=5432 \
python manage.py migrate
```

If Django tries to connect to `localhost:5432` on Railway, `DATABASE_URL` is not
being read by the deployed code or is not set on the Django service.

## Production start command

For Railway, the Django service start command should run migrations and then
start Gunicorn:

```bash
python manage.py migrate && gunicorn config.wsgi
```

Gunicorn is the production WSGI server for Django. It is listed in
`requirements.txt` so Railway installs it during deployment.

The `server.sh` script starts PostgreSQL for you, but the underlying command is:

```bash
docker compose up -d db
```

The script stops PostgreSQL with:

```bash
docker compose down
```
