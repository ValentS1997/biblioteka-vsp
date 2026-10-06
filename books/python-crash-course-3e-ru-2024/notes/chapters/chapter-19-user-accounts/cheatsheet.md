# Шпаргалка главы 19 — Учетные записи пользователей

## ModelForm

~~~python
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}
~~~

Entry form:

~~~python
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {
            'text': forms.Textarea(
                attrs={'cols': 80}
            )
        }
~~~

## GET / POST pattern

~~~python
if request.method != 'POST':
    form = TopicForm()
else:
    form = TopicForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('learning_logs:topics')
~~~

Invalid form falls through to rendering with errors.

## CSRF

Every POST form shown by source contains:

~~~django
{% csrf_token %}
~~~

## Create related Entry

~~~python
new_entry = form.save(commit=False)
new_entry.topic = topic
new_entry.save()
~~~

## Edit existing Entry

GET:

~~~python
form = EntryForm(instance=entry)
~~~

POST:

~~~python
form = EntryForm(
    instance=entry,
    data=request.POST,
)
~~~

## Authentication

Built-in URLs:

~~~python
path(
    '',
    include('django.contrib.auth.urls')
)
~~~

Settings:

~~~python
LOGIN_REDIRECT_URL = 'learning_logs:index'
LOGOUT_REDIRECT_URL = 'learning_logs:index'
LOGIN_URL = 'accounts:login'
~~~

## Register + automatic login

~~~python
form = UserCreationForm(data=request.POST)

if form.is_valid():
    new_user = form.save()
    login(request, new_user)
    return redirect('learning_logs:index')
~~~

## Authorization layers

1. Authentication gate:

~~~python
@login_required
def topics(request):
    ...
~~~

2. List filtering:

~~~python
Topic.objects.filter(
    owner=request.user
)
~~~

3. Object ownership:

~~~python
if topic.owner != request.user:
    raise Http404
~~~

4. Creation ownership:

~~~python
new_topic = form.save(commit=False)
new_topic.owner = request.user
new_topic.save()
~~~

## Security invariant

Being logged in is not enough.

Private object access requires both:
- authenticated user;
- ownership check for the requested object.

Exercise 19.4 identifies `new_entry/<topic_id>/` as another path that must enforce ownership.
