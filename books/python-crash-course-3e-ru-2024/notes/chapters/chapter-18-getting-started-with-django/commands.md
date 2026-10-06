# Команды и операции главы 18

## Create virtual environment

~~~bash
python -m venv ll_env
~~~

Classification: **filesystem state-changing**.

Effect: creates directory `ll_env`.

Before running:
- current directory: `[Needs confirmation]`;
- interpreter version: `[Needs confirmation]`.

Rollback:

~~~bash
rm -rf -- ll_env
~~~

Risk: destructive. Run only after verifying the target path is the intended virtual environment and contains no user data.

## Activate environment

Linux/macOS source example:

~~~bash
source ll_env/bin/activate
~~~

Windows source example:

~~~text
ll_env\Scripts\activate
~~~

PowerShell note: source says `Activate` begins with uppercase letter.

Verification: shell prompt includes `(ll_env)`.

## Deactivate

~~~bash
deactivate
~~~

Classification: shell-environment state change only.

## Upgrade pip

~~~bash
pip install --upgrade pip
~~~

Classification: **state-changing package-management action inside venv**.

Current version/rollback: `[Needs confirmation]`.

## Install Django

~~~bash
pip install django
~~~

Optional source pin:

~~~bash
pip install 'django==4.1.*'
~~~

Classification: state-changing package-management action inside venv.

## Create Django project

~~~bash
django-admin startproject ll_project .
~~~

Classification: **filesystem state-changing**.

Important source requirement: trailing dot.

Verification:

~~~bash
ls
ls ll_project
~~~

Expected source layout includes `manage.py` and project package.

Rollback guidance in source: if dot was omitted, delete generated files/folders except `ll_env` and retry.

Because deletion is destructive, exact generated paths must be confirmed before cleanup.

## Initial database migration

~~~bash
python manage.py migrate
~~~

Classification: **database/file state-changing**.

Effect in source SQLite setup: creates/updates `db.sqlite3`.

Verification: migrations end with `OK`; file appears in project directory.

Rollback strategy for an existing database: `[Needs confirmation]`.

## Development server

~~~bash
python manage.py runserver
~~~

Classification: local network/listening workload.

Source default:
- `127.0.0.1:8000`;
- stop with `Ctrl+C`.

Alternate port:

~~~bash
python manage.py runserver 8001
~~~

Used when port 8000 is already in use.

## Create app

~~~bash
python manage.py startapp learning_logs
~~~

Classification: filesystem state-changing.

Verification: `learning_logs/` contains models/admin/apps/migrations/tests/views files.

## Create migrations

~~~bash
python manage.py makemigrations learning_logs
python manage.py migrate
~~~

Classification: migration-file + database state-changing.

Acceptance:
- new migration file generated;
- corresponding migration applies `OK`.

## Create superuser

~~~bash
python manage.py createsuperuser
~~~

Classification: **privileged application-data state-changing**.

Credentials are interactive and must not be embedded in artifacts.

Verification: source expects `Superuser created successfully.`

## Django shell

~~~bash
python manage.py shell
~~~

Classification: interactive application shell. Queries can be read-only or state-changing depending on entered code.

Source examples are read-only ORM queries.

## Runserver troubleshooting

Source guidance:
- if page unavailable, verify server still runs;
- restart `runserver`;
- if port busy, try another port.

No production deployment inference should be drawn from the development server.
