# Диаграмма — глава 18

## Project setup

~~~mermaid
flowchart TD
    A["create venv"] --> B["activate"]
    B --> C["install Django"]
    C --> D["startproject ll_project ."]
    D --> E["migrate"]
    E --> F["runserver"]
    F --> G["startapp learning_logs"]
~~~

## Model lifecycle

~~~mermaid
flowchart LR
    A["edit models.py"] --> B["makemigrations"]
    B --> C["migration file"]
    C --> D["migrate"]
    D --> E["SQLite schema updated"]
    E --> F["admin / ORM use"]
~~~

## Request routing

~~~mermaid
flowchart LR
    A["browser URL"] --> B["project urls.py"]
    B --> C["app urls.py"]
    C --> D["view function"]
    D --> E["ORM query/context"]
    E --> F["template"]
    F --> G["HTTP response"]
~~~

## Topic detail

~~~mermaid
flowchart TD
    A["/topics/<topic_id>/"] --> B["views.topic(request, topic_id)"]
    B --> C["Topic.objects.get(id=topic_id)"]
    C --> D["topic.entry_set.order_by('-date_added')"]
    D --> E["context: topic + entries"]
    E --> F["topic.html"]
~~~
