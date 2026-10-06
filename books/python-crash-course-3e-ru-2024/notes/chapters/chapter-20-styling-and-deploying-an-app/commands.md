# Команды и операции главы 20

Все команды ниже поддержаны RAG главы 20. Значения из листингов книги являются примерами и не должны переноситься в реальную среду без проверки.

## Python dependencies

~~~bash
pip install django-bootstrap5
~~~

Classification: state-changing.

Effect: устанавливает django-bootstrap5 в активную виртуальную среду.

Verification: source затем добавляет django_bootstrap5 в INSTALLED_APPS и использует его template tags.

Rollback: [Needs confirmation].

~~~bash
pip install platformshconfig
~~~

Classification: state-changing.

Effect: устанавливает helper для определения Platform.sh environment.

Verification: settings.py импортирует Config from platformshconfig.

Rollback: [Needs confirmation].

## Platform.sh CLI installer

Source предоставляет installer через curl с передачей результата интерпретатору PHP.

Classification: state-changing.

Effect/risk: выполняется удаленно полученный installer; точный набор изменений [Needs confirmation].

Source после установки требует перезапустить terminal. Exact rollback: [Needs confirmation].

## Dependency snapshots

~~~bash
pip freeze > requirements.txt
~~~

Classification: state-changing filesystem operation.

Effect: создает или перезаписывает requirements.txt текущим package set.

Verification: открыть файл и проверить package names/versions.

Source example содержит asgiref, beautifulsoup4, Django, django-bootstrap5, platformshconfig, soupsieve и sqlparse. Source отдельно требует использовать реально установленные версии, если они отличаются от примера.

Rollback: previous Git version, если она уже существовала; иначе [Needs confirmation].

Source также создает requirements_remote.txt:

~~~text
gunicorn
psycopg2
~~~

Classification: state-changing filesystem operation.

## Platform.sh build/deploy hooks

.platform.app.yaml build hook:

~~~bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements_remote.txt
mkdir logs
python manage.py collectstatic
rm -rf logs
~~~

Classification: state-changing.

Verification: source ожидает эти шаги в output deployment build.

Rollback: [Needs confirmation].

Deploy hook:

~~~bash
python manage.py migrate
~~~

Classification: state-changing database operation.

Verification: successful deployment.

Rollback: [Needs confirmation].

## Git checks and setup

~~~bash
git --version
~~~

Classification: read-only.

~~~bash
git config --global user.name "eric"
git config --global user.email "eric@example.com"
~~~

Classification: state-changing user-level Git configuration.

Source identity values are examples.

Rollback: [Needs confirmation].

Project initialization:

~~~bash
git init
git add .
git commit -am "Ready for deployment to Platform.sh."
~~~

Classification: state-changing.

Verification:

~~~bash
git status
~~~

Classification: read-only.

Source acceptance before deployment:

~~~text
On branch main
nothing to commit, working tree clean
~~~

Exact rollback command is not supplied by the chapter: [Needs confirmation].

## Platform.sh authentication and project creation

~~~bash
platform login
~~~

Classification: interactive authentication/local configuration.

Source may offer to create SSH configuration. Credentials and SSH material must not be recorded in artifacts.

~~~bash
platform create
~~~

Classification: state-changing remote operation.

Effect: creates a Platform.sh project and may add it as Git remote.

Source project title, region, plan, environment count, storage and cost are environment/account-specific examples.

Verification: source receives "The project is now ready!".

Rollback: source later provides project deletion.

## Deploy current HEAD

~~~bash
platform push
~~~

Classification: state-changing remote deployment/workload-generating.

Effect: pushes HEAD to the production branch and triggers build/deploy.

Verification:

~~~bash
platform url
~~~

Classification: read-only/discovery.

Then open the deployed application and verify expected behavior.

Deployment rollback command: [Needs confirmation].

## Remote administration

~~~bash
platform environment:ssh
~~~

Classification: interactive remote session.

Inside that session:

~~~bash
ls
~~~

Classification: read-only.

Create production administrator:

~~~bash
python manage.py createsuperuser
~~~

Classification: state-changing database operation.

Credentials/passwords must not be copied to artifacts.

Verification: source expects successful superuser creation.

Exit remote shell:

~~~bash
exit
~~~

Classification: session control.

## Production hardening deployment

After adding DEBUG = False in Platform.sh-specific settings:

~~~bash
git commit -am "Set DEBUG False on live site."
git status
platform push
~~~

Classification:
- commit: state-changing;
- status: read-only;
- push: state-changing deployment.

Acceptance:
- Git working tree clean before push;
- deployed /topics/999/ returns generic Server Error (500);
- Django debug details are not exposed.

## Custom error pages

After creating root templates/404.html and templates/500.html:

~~~bash
git add .
git commit -am "Added custom 404 and 500 error pages."
platform push
~~~

Classification: state-changing.

Verification: deployed error pages use project styling.

Rollback: [Needs confirmation].

## Ongoing deployment loop

When new files are created:

~~~bash
git add .
~~~

Then:

~~~bash
git commit -am "message"
platform push
~~~

Classification: state-changing.

Verification: visit deployed project and confirm intended changes.

## Remove deployed project

Source provides a Platform.sh CLI project-deletion operation and explicitly describes it as destructive and confirmation-gated.

Classification: destructive remote state-changing operation.

Effect on local project: source says none.

Rollback: not provided.

## Inspect/remove Platform.sh Git remote

~~~bash
git remote
~~~

Classification: read-only.

Source expected remote name: platform.

~~~bash
git remote remove platform
~~~

Classification: state-changing local Git configuration.

Effect: removes the Platform.sh remote URL reference from local repository.

Verification: run git remote again.

Rollback: [Needs confirmation].
