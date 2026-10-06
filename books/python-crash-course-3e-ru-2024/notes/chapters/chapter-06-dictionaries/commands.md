# Операции и методы главы 6

Только source-confirmed конструкции из `e0015:c01–c12`.

## Доступ и изменение

| Конструкция | Тип | Effect | Risk | Verification | Rollback |
|---|---|---|---|---|---|
| `d[key]` | read-only | получает значение | отсутствующий ключ → `KeyError` | вывести значение | `[Not applicable]` |
| `d.get(key, default)` | read-only | значение либо default | может скрыть отсутствие обязательного ключа, если применить не по намерению | проверить существующий/отсутствующий ключ | `[Not applicable]` |
| `d[new_key] = value` | state-changing | добавляет пару | меняет словарь | вывести словарь | `[Needs confirmation]` |
| `d[key] = new_value` | state-changing | меняет значение | прежнее значение может быть потеряно | вывести ключ | `[Needs confirmation]` |
| `del d[key]` | state-changing | удаляет ключ и значение | источник: отменить нельзя | вывести словарь / проверить ключ | rollback отсутствует по source |

## get()

~~~python
alien_0 = {'color': 'green', 'speed': 'slow'}
point_value = alien_0.get('points', 'No point value assigned.')
~~~

При отсутствии `points` возвращается указанное сообщение.

Без второго аргумента источник указывает возврат `None`.

## Перебор

~~~python
for key, value in user_0.items():
    ...
~~~

Классификация: workload-generating iteration.

~~~python
for name in favorite_languages.keys():
    ...
~~~

Источник также допускает:

~~~python
for name in favorite_languages:
    ...
~~~

### Сортированный обход ключей

~~~python
for name in sorted(favorite_languages.keys()):
    ...
~~~

Классификация: workload-generating + read-only transformation.

### Значения

~~~python
for language in favorite_languages.values():
    ...
~~~

Повторы сохраняются.

### Уникальные значения

~~~python
for language in set(favorite_languages.values()):
    ...
~~~

Классификация: read-only transformation + iteration.

Источник также показывает literal set:

~~~python
languages = {'python', 'rust', 'python', 'c'}
~~~

## Nesting

### Список словарей

~~~python
aliens = [alien_0, alien_1, alien_2]
~~~

### Генерация списка словарей

~~~python
aliens = []

for alien_number in range(30):
    new_alien = {'color': 'green', 'points': 5, 'speed': 'slow'}
    aliens.append(new_alien)
~~~

### Список как значение словаря

~~~python
pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese'],
}
~~~

### Словарь как значение словаря

~~~python
users = {
    'aeinstein': {
        'first': 'albert',
        'last': 'einstein',
        'location': 'princeton',
    },
}
~~~

## Source findings affecting code

Не нормализовать молча:

~~~python
alien_0['speed'] = fast
~~~

Источник показывает эту строку в `e0015:c03`; см. `source-findings.md`.

Также source dictionary/output расходятся для Edward в примере nested favorite languages; см. отдельный finding.
