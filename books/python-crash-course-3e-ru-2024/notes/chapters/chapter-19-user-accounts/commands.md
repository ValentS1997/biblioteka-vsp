# Команды и операции главы 19

## Create accounts app

~~~bash
python manage.py startapp accounts
~~~

Classification: filesystem state-changing.

Verification: source expects new `accounts/` directory with standard app files.

## Django auth routes

No separate command; source adds:

~~~python
path(
    'accounts/',
    include('accounts.urls')
)
~~~

and inside accounts URLs:

~~~python
path(
    '',
    include('django.contrib.auth.urls')
)
~~~

## Registration

`UserCreationForm.save()` creates user data in the database.

Classification: application/database state-changing.

Credentials/passwords are user input and must not be recorded in artifacts.

## Add Topic.owner

Source model change:

~~~python
owner = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
)
~~~

Effect: Topic requires an owner; deleting User cascades to related Topic records according to source model.

## Identify real user IDs before migration

~~~bash
python manage.py shell
~~~

Source read-only queries:

~~~python
from django.contrib.auth.models import User

User.objects.all()

for user in User.objects.all():
    print(user.username, user.id)
~~~

The source IDs `1`, `2`, `3` are examples only.

Acceptance before migration: choose an ID that actually exists in the target database.

## Create owner migration

~~~bash
python manage.py makemigrations learning_logs
~~~

Classification: migration-file state-changing and interactive schema-planning action.

Source scenario:
- Django detects non-nullable `owner` on existing Topic rows;
- select one-off default;
- enter a valid existing user ID.

Exact ID: `[Needs confirmation]`.

## Apply migration

~~~bash
python manage.py migrate
~~~

Classification: database state-changing.

Verification:
- migration reports `OK`;
- shell query confirms each Topic has intended owner.

Rollback strategy for a real populated DB: `[Needs confirmation]`.

## Verify ownership

~~~python
from learning_logs.models import Topic

for topic in Topic.objects.all():
    print(topic, topic.owner)
~~~

Classification: read-only ORM verification.

## Destructive alternative mentioned by source

~~~bash
python manage.py flush
~~~

Classification: **destructive database operation**.

Source explicitly warns:
- all existing data are lost;
- a new superuser must be created afterward.

This is not a routine rollback recommendation.

## Form saves

~~~python
form.save()
form.save(commit=False)
~~~

Classification: application/database state-changing when final save occurs.

`commit=False` creates an unsaved model instance so required relationships can be assigned first.
