# Шпаргалка главы 20

## Symptom / problem framing

Исходное состояние главы:

- приложение «Журнал обучения» функционально;
- оформление еще не приведено к единому профессиональному виду;
- приложение работает только локально;
- production-specific settings и deployment configuration еще не подготовлены.

Цель главы:

- оформить Django templates через Bootstrap/django-bootstrap5;
- описать зависимости и Platform.sh configuration;
- зафиксировать рабочее состояние в Git;
- развернуть проект;
- проверить deployment;
- отключить DEBUG на рабочем сервере;
- добавить собственные 404/500 pages.

## Baseline / context

Source boundary:

- e0030:c01–e0030:c19
- EPUB spine item 30
- OEBPS/Text/978544614112-27.xhtml

Baseline application уже содержит Learning Log, accounts, authentication и ownership logic из предыдущих глав.

Presentation layer не должен менять основную функциональность приложения: source прямо показывает, что при оформлении topic page изменяются HTML/Bootstrap elements, а Django data logic остается прежней.

## Read-only checks

### Git installed

~~~bash
git --version
~~~

Classification: read-only.

Expected source behavior: вывод версии Git или сообщение, что Git не установлен.

### Repository state before deployment

~~~bash
git status
~~~

Classification: read-only.

Acceptance before push: source ожидает clean working tree.

### Remote names

~~~bash
git remote
~~~

Classification: read-only.

Используется перед удалением Platform.sh remote reference.

### Deployed URL

~~~bash
platform url
~~~

Classification: read-only/discovery against deployed environment.

Expected behavior: CLI перечисляет URLs проекта и позволяет открыть выбранный.

### Remote filesystem after SSH

~~~bash
ls
~~~

Classification: read-only.

Source выполняет эту команду внутри platform environment:ssh для проверки файлов развернутого проекта.

## Interpretation

### Styling

django-bootstrap5 добавляет template tags для Bootstrap CSS/JavaScript, form rendering и buttons.

base.html становится общей оболочкой:

- navbar;
- responsive collapse;
- account links/logout form;
- page_header;
- content.

Отдельные templates получают компоненты Bootstrap:

- index: jumbotron-like lead block;
- login: bootstrap_form + bootstrap_button;
- topics: list-group;
- topic entries: card.

### Deployment

Воспроизводимое развертывание строится из четырех частей:

1. Python dependencies.
2. Platform.sh YAML configuration.
3. Platform-specific Django settings.
4. Git snapshot, отправляемый на remote platform.

requirements.txt фиксирует локальные packages/versions.

requirements_remote.txt добавляет production packages gunicorn и psycopg2.

.platform.app.yaml определяет runtime, Postgres relationship, gunicorn start command, static location, disk, mount и build/deploy hooks.

.platform/routes.yaml определяет request routing.

.platform/services.yaml определяет Postgres service.

### Production boundary

Source использует platformshconfig.Config, чтобы применять удаленные settings только внутри Platform.sh environment.

Production-specific changes включают:

- ALLOWED_HOSTS;
- STATIC_ROOT;
- SECRET_KEY;
- Postgres DATABASES;
- DEBUG = False.

## Next action

После работающего локального приложения source sequence таков:

1. Подключить django-bootstrap5.
2. Привести templates к общему Bootstrap layout.
3. Установить Platform.sh tooling/platformshconfig.
4. Зафиксировать requirements.
5. Создать Platform.sh YAML files.
6. Добавить Platform-specific settings.
7. Настроить Git и .gitignore.
8. Убедиться, что Git working tree clean.
9. Создать Platform.sh project.
10. Выполнить platform push.
11. Проверить deployed URL.
12. Создать remote superuser.
13. Установить DEBUG = False только для deployed environment.
14. Commit → status → push → verification.
15. Добавить custom 404/500 templates и повторить deployment cycle.

## Modifying action

### Install django-bootstrap5

~~~bash
pip install django-bootstrap5
~~~

Effect: изменяет active Python environment.

Verification: import/use через INSTALLED_APPS и template tags; source затем проверяет pages в browser.

Rollback: [Needs confirmation].

### Install platformshconfig

~~~bash
pip install platformshconfig
~~~

Effect: изменяет active Python environment.

Verification: settings.py использует Config.

Rollback: [Needs confirmation].

### Generate dependency snapshot

~~~bash
pip freeze > requirements.txt
~~~

Effect: перезаписывает requirements.txt.

Verification: открыть файл и проверить package list/versions.

Rollback: восстановить предыдущую Git version, если она уже была зафиксирована; иначе [Needs confirmation].

### Git snapshot

~~~bash
git init
git add .
git commit -am "Ready for deployment to Platform.sh."
~~~

Effect: создает repository metadata, stages files и создает commit.

Verification:

~~~bash
git status
~~~

Acceptance: clean working tree.

Rollback: source не задает rollback для initialization/commit; [Needs confirmation].

### Deploy

~~~bash
platform push
~~~

Effect: отправляет HEAD в production branch Platform.sh и запускает build/deploy flow.

Source-observed build/deploy includes dependency installation, collectstatic and migrate.

Verification:

~~~bash
platform url
~~~

Затем открыть deployed application и проверить ожидаемое изменение.

Rollback: source не задает deployment rollback command; [Needs confirmation].

### Disable DEBUG on production

Platform-specific settings.py:

~~~python
if config.is_valid_platform():
    ALLOWED_HOSTS.append('.platformsh.site')
    DEBUG = False
~~~

Effect: production error responses больше не показывают Django debug detail.

Verification: source повторно открывает /topics/999/ и ожидает generic Server Error (500) без project/server debug information.

Rollback: source не задает production rollback; [Needs confirmation].

### Delete Platform.sh project

~~~bash
platform project:delete
~~~

Effect: destructive — удаляет remote project.

Verification: project больше не должен оставаться активным на Platform.sh; source также предлагает проверить dashboard.

Rollback: не предоставлен; удаление описано как destructive.

## Verification / acceptance checks

Styling:

- navbar присутствует и сворачивается при узком viewport;
- login form и errors оформлены через Bootstrap;
- topics используют list-group;
- entries используют cards;
- existing Django functionality не должна измениться.

Pre-deploy:

- requirements files созданы;
- Platform.sh config files созданы;
- settings.py содержит conditional Platform.sh section;
- .gitignore исключает virtualenv, __pycache__ и SQLite;
- git status сообщает clean working tree.

Deployment:

- platform push завершается без ошибки;
- platform url возвращает deployed URL;
- application открывается удаленно;
- remote database initially separate from local data;
- remote superuser создается через SSH session.

Security:

- DEBUG = False применяется только к deployed Platform.sh environment;
- /topics/999/ больше не показывает debug details;
- custom 404/500 templates оформлены в общем стиле.

## Rollback

Source-supported rollback coverage ограничена.

- Git описывается как механизм возврата к последнему работоспособному snapshot, но exact rollback command в главе не приводится.
- Для failed deployment source предлагает исправить configuration/code, выполнить новый commit и повторить platform push.
- platform project:delete удаляет remote deployment полностью и не изменяет local project.
- git remote remove platform удаляет только remote URL reference из local repository.

Для остальных state-changing действий exact rollback: [Needs confirmation].
