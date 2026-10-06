# Разбор упражнений главы 17

Это RAG-grounded решения/шаблоны, не официальный ключ издателя. Live APIs здесь не вызывались.

## 17.1. Другие языки

Source-supported change — заменить language value в query.

Пример для Go:

~~~python
url = "https://api.github.com/search/repositories"
url += "?q=language:go+sort:stars+stars:>10000"
~~~

Для других source-listed languages меняется только query term.

Acceptance:
- `status_code` проверен;
- `incomplete_results` проверен;
- chart построен из фактически returned repositories.

Конкретные counts/stars/order: `[Needs confirmation]`.

## 17.2. Активные обсуждения

Source даёт необходимые fields:
- `title`;
- `hn_link`;
- `comments`.

Сначала пропускаем records без `descendants`:

~~~python
submission_dicts = []

for submission_id in submission_ids[:30]:
    url = (
        "https://hacker-news.firebaseio.com/v0/"
        f"item/{submission_id}.json"
    )
    r = requests.get(url)
    response_dict = r.json()

    try:
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': (
                "http://news.ycombinator.com/"
                f"item?id={submission_id}"
            ),
            'comments': response_dict['descendants'],
        }
    except KeyError:
        continue
    else:
        submission_dicts.append(submission_dict)
~~~

Chart inputs по patterns главы:

~~~python
article_links, comments = [], []

for submission_dict in submission_dicts:
    title = submission_dict['title']
    link = submission_dict['hn_link']
    article_links.append(
        f"<a href='{link}'>{title}</a>"
    )
    comments.append(submission_dict['comments'])

fig = px.bar(
    x=article_links,
    y=comments,
)
fig.show()
~~~

Точные live stories/comment counts: `[Needs confirmation]`.

## 17.3. Тестирование python_repos.py

Самодостаточный вариант с общим request helper:

~~~python
import requests

def get_response():
    url = "https://api.github.com/search/repositories"
    url += "?q=language:python+sort:stars+stars:>10000"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    return requests.get(url, headers=headers)

def test_status_code():
    r = get_response()
    assert r.status_code == 200

def test_response_has_items():
    r = get_response()
    response_dict = r.json()

    assert 'items' in response_dict
    assert len(response_dict['items']) > 0
~~~

Первый test — обязательная source check. Второй использует только структуру response, уже показанную в главе, и не фиксирует динамический repository count.

Это **live network test**, поэтому результат зависит от доступности API, current API contract и rate-limit state. Каждый test выше выполняет отдельный request и расходует соответствующую квоту.

Source предлагает также проверить expected item count и total-count threshold, но конкретные значения не задаёт: `[Needs confirmation]`.

## 17.4. Дальнейшие исследования

Требуется информация из external documentation.

В `rag_only`:
- новые Plotly formatting options: `[Needs confirmation]`;
- дополнительные GitHub/HN endpoints: `[Needs confirmation]`;
- другие public APIs: `[Needs confirmation]`.

Source purpose — самостоятельно расширить уже построенный request → parse → visualize pipeline.
