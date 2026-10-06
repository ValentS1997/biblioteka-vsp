# Глава 11. Модули

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 11 — «Модули». Она переносит идею повторного использования от функций к
отдельным Python-файлам и пакетам. Источник разбирает `import`, `sys.argv`,
`sys.path`, bytecode `.pyc`, `from ... import ...`, `__name__`, создание
собственных модулей, `dir()`, `del` и package hierarchy с `__init__.py`.

Разделы, подтверждённые RAG:

- вводная часть: module reuse и `sys`
- 11.1 Файлы байткода `.pyc`
- 11.2 Оператор `from ... import ...`
- 11.3 Имя модуля — `__name__`
- 11.4 Создание собственных модулей
- 11.5 Функция `dir`
- 11.6 Пакеты
- 11.7 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0079:c01` — `p0086:c01`
- PDF pages: 79–86
- printed pages visible in chapter: 71–78
- chapter start: PDF page 79, heading «Модули»
- chapter end: PDF page 86, section 11.7 «Резюме»
- next chapter boundary: PDF page 87 begins «Структуры данных»
- boundary verified: yes

## Main principle

Модуль — reusable program unit. Самый простой source model: Python-файл `.py` с
функциями и переменными, который можно импортировать в другую программу. Пакеты
добавляют иерархию каталогов поверх модулей.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| Intro | `import sys`, `sys.argv`, `sys.path`, module initialization on first import. |
| 11.1 | `.pyc` as byte-compiled intermediate form intended to speed later imports. |
| 11.2 | `from module import name` and wildcard import; source recommends preferring plain `import` to avoid name conflicts. |
| 11.3 | `__name__ == '__main__'` distinguishes direct execution from import. |
| 11.4 | Any `.py` program can serve as a module; own module example uses `mymodule.py`, dotted access and `__version__`. |
| 11.5 | `dir()` lists identifiers/attributes; `del` removes a name from current module scope. |
| 11.6 | Packages are directories containing modules and special `__init__.py` files in the source model. |
| 11.7 | Modules are reusable programs; packages hierarchically organize modules. |

## Core examples

### using_sys.py

```python
import sys

print('Аргументы командной строки:')
for i in sys.argv:
    print(i)

print('\n\nПеременная PYTHONPATH содержит', sys.path, '\n')
```

Source execution:

```text
python3 using_sys.py we are arguments
```

### __name__

```python
if __name__ == '__main__':
    print('Эта программа запущена сама по себе.')
else:
    print('Меня импортировали в другой модуль.')
```

### own module

```python
def sayhi():
    print('Привет! Это говорит мой модуль.')

__version__ = '0.1'
```

Usage:

```python
import mymodule

mymodule.sayhi()
print('Версия', mymodule.__version__)
```

### dir / del

```python
import sys
dir(sys)
dir()
a = 5
dir()
del a
dir()
```

## Operational acceptance

После главы читатель должен уметь:

- импортировать module и обращаться к его members через точку;
- объяснить роль `sys.argv` и `sys.path` в source framing;
- отличить plain `import` от `from ... import ...`;
- использовать `__name__ == '__main__'`;
- создать `.py` module и импортировать его;
- использовать `dir()` для просмотра names;
- объяснить effect `del name`;
- описать source package hierarchy с `__init__.py`.

## Safety / integrity boundary

- Import выполняет top-level code модуля при первом import по source explanation;
  следовательно, импорт может быть workload-generating и иметь side effects.
- Source сообщает, что `.pyc` может создаваться автоматически при import; это
  filesystem side effect, а не чисто read-only operation.
- Создание `mymodule.py`, demo files и package directory tree меняет filesystem state;
  explicit rollback source не задан.
- `del a` изменяет runtime namespace.
- Source mixes `python3 using_sys.py` / `python3 using_name.py` with prose/example
  variants using `python`; variants are not normalized.
- Historical `.pyc` placement and `sys.path/PYTHONPATH` statements are preserved as
  source claims, not current verified runtime rules.

## Conditional artifacts

Раздел 11.7 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
