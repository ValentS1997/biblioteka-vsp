# Разбор упражнений главы 19

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Django runtime здесь не запускался.

## 19.1. Блог

Source не задаёт exact model names/fields, поэтому canonical answer не должен выдумывать их.

Минимальный process contract по patterns глав 18–19:

~~~text
create project/app
    ↓
define two models
    ↓
INSTALLED_APPS
    ↓
makemigrations + migrate
    ↓
register models in admin
    ↓
create sample data
    ↓
URL → view → template
    ↓
ModelForms for create/edit
~~~

Нужно отдельно определить:
- имя/fields «blog» model: `[Needs confirmation]`;
- имя/fields publication model: `[Needs confirmation]`;
- exact chronological field/order: `[Needs confirmation]`.

## 19.2. Учетные записи в блоге

Можно перенести source auth pattern:

~~~python
path(
    'accounts/',
    include('accounts.urls')
)
~~~

и:

~~~python
path(
    '',
    include('django.contrib.auth.urls')
)
~~~

Header logic:

~~~django
{% if user.is_authenticated %}
  Hello, {{ user.username }}.
{% else %}
  <a href="{% url 'accounts:register' %}">
    Register
  </a>
  <a href="{% url 'accounts:login' %}">
    Log in
  </a>
{% endif %}
~~~

Registration flow может повторять `UserCreationForm` из главы.

## 19.3. Рефакторинг

Source уже использует ownership rule:

~~~python
if topic.owner != request.user:
    raise Http404
~~~

Refactor, прямо требуемый exercise:

~~~python
def check_topic_owner(topic, user):
    if topic.owner != user:
        raise Http404
~~~

Then:

~~~python
topic = Topic.objects.get(id=topic_id)
check_topic_owner(topic, request.user)
~~~

и для Entry:

~~~python
entry = Entry.objects.get(id=entry_id)
topic = entry.topic
check_topic_owner(topic, request.user)
~~~

Exact helper placement in `views.py` source exercise не ограничивает.

## 19.4. Защита new_entry

Проверка должна происходить после загрузки Topic и до обработки/saving Entry form:

~~~python
@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)

        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()

            return redirect(
                'learning_logs:topic',
                topic_id=topic_id,
            )

    context = {
        'topic': topic,
        'form': form,
    }

    return render(
        request,
        'learning_logs/new_entry.html',
        context,
    )
~~~

Это закрывает cross-user path, прямо указанную в exercise 19.4.

## 19.5. Защищенный блог

Source задаёт security behavior, но не exact Blog model design.

Canonical authorization pattern:

~~~text
public list/detail read
    ↓
authenticated create
    ↓
post.owner = request.user
    ↓
authenticated edit
    ↓
if post.owner != request.user:
    raise Http404
~~~

Для create, по аналогии с Topic:

~~~python
new_post = form.save(commit=False)
new_post.owner = request.user
new_post.save()
~~~

Для edit:

~~~python
if post.owner != request.user:
    raise Http404
~~~

Exact Post model/route names: `[Needs confirmation]`.
