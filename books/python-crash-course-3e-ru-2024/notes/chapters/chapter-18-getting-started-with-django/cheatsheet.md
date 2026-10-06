# Шпаргалка главы 18 — Знакомство с Django

## Environment

~~~bash
python -m venv ll_env
source ll_env/bin/activate
pip install --upgrade pip
pip install django
~~~

Source pin option:

~~~bash
pip install 'django==4.1.*'
~~~

Current compatibility/version: `[Needs confirmation]`.

## Project bootstrap

~~~bash
django-admin startproject ll_project .
python manage.py migrate
python manage.py runserver
~~~

Expected source artifacts:
- `manage.py`;
- `ll_project/settings.py`;
- `ll_project/urls.py`;
- `db.sqlite3` after migrate.

## App bootstrap

~~~bash
python manage.py startapp learning_logs
~~~

Key files:
- `models.py`;
- `admin.py`;
- `views.py`;
- `migrations/`.

## Model pattern

~~~python
class Topic(models.Model):
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
~~~

~~~python
class Entry(models.Model):
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.text[:50]}..."
~~~

## Migration invariant

~~~text
change models.py
      ↓
makemigrations learning_logs
      ↓
migration file
      ↓
migrate
      ↓
database schema updated
~~~

## ORM shell

~~~python
Topic.objects.all()
Topic.objects.get(id=1)
t.entry_set.all()
~~~

Reverse relation pattern:

~~~text
<lowercase-related-model>_set
~~~

## URL → View → Template

Project URL:

~~~python
path('', include('learning_logs.urls'))
~~~

App URL:

~~~python
path('', views.index, name='index')
path('topics/', views.topics, name='topics')
path(
    'topics/<int:topic_id>/',
    views.topic,
    name='topic',
)
~~~

## Context

~~~python
topics = Topic.objects.order_by('date_added')
context = {'topics': topics}
return render(
    request,
    'learning_logs/topics.html',
    context,
)
~~~

## Template inheritance

Base:

~~~django
<a href="{% url 'learning_logs:index' %}">
  Learning Log
</a>

{% block content %}{% endblock content %}
~~~

Child:

~~~django
{% extends "learning_logs/base.html" %}

{% block content %}
  ...
{% endblock content %}
~~~

## Verification checklist

- venv active before install/project work;
- project created in intended directory;
- migrations show OK;
- development server binds expected local port;
- app listed in `INSTALLED_APPS`;
- models registered before admin use;
- ORM queries return expected records;
- named URLs resolve;
- views pass intended context;
- templates render empty-state messages where source specifies.
