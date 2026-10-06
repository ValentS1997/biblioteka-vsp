# Глава 6. Первые шаги

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 6 — «Первые шаги». Она переводит читателя от установленного Python к первой
реальной программе и показывает два способа выполнения кода: интерактивный
интерпретатор и файл программы. Затем рассматриваются выбор редактора, запуск
`helloworld.py`, Unix-executable scripts, `PATH` и встроенная справка `help()`.

Разделы, подтверждённые RAG:

- 6.1 Введение
- 6.2 Использование командной строки интерпретатора
- 6.3 Выбор редактора
- 6.4 Использование программных файлов
  - 6.4.1 Исполнимые программы на Python
- 6.5 Получение помощи
- 6.6 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0035:c01` — `p0042:c01`
- PDF pages: 35–42
- printed pages visible in chapter: 27–34
- chapter start: PDF page 35, heading «Первые шаги»
- chapter end: PDF page 42, chapter footer after section 6.6
- next chapter boundary: PDF page 43 begins «Основы»
- boundary verified: yes

## Main principle

Глава строит минимальный feedback loop для начинающего:

1. запустить Python;
2. выполнить выражение интерактивно;
3. сохранить ту же идею в `.py`-файл;
4. выполнить файл и сверить вывод;
5. при ошибке проверить точность кода, регистр и начальные отступы;
6. научиться получать встроенную справку;
7. для Unix-подобных систем — при необходимости сделать script исполнимым и доступным
   через `PATH`.

## Chapter map

| Section | Source-grounded purpose |
|---|---|
| 6.1 | Два режима: interactive prompt и program file. |
| 6.2 | Запуск `python3`, приглашение `>>>`, первый `print(...)`, способы выхода. |
| 6.3 | Критерии редактора: прежде всего syntax highlighting и automatic indentation; source рекомендует Komodo Edit новичкам и упоминает Vim/Emacs для опытных. |
| 6.4 | Создание `helloworld.py`, выбор каталога, запуск через `python3 helloworld.py`, разбор результата. |
| 6.4.1 | Shebang, executable bit, прямой запуск, просмотр/изменение `PATH`, копирование script в каталог из `PATH`. |
| 6.5 | Встроенная `help`: `help(print)`, `help()`, `help('return')`; выход из help по `q`. |
| 6.6 | Резюме: читатель умеет писать, сохранять и запускать Python-программы. |

## Source-confirmed code

Минимальная программа в файловом варианте:

```python
print('Привет, Мир!')
```

Unix shebang variant:

```python
#!/usr/bin/env python3
print('Привет, Мир!')
```

## Operational acceptance

Основная source-confirmed проверка для файлового варианта:

```text
python3 helloworld.py
```

Ожидаемый результат в книге:

```text
Привет, Мир!
```

Для executable variant source показывает прямой запуск `./helloworld.py` с тем же
результатом.

## Safety boundary

- `mkdir`, `chmod`, `cp` и assignment `PATH=...` изменяют состояние
  filesystem/session и классифицированы отдельно в `commands.md`.
- Source-specific rollback для этих изменений не приведён — `[Needs confirmation]`.
- Каталоги `/tmp/py`, `/home/swaroop/bin`, `/home/swaroop/mydir`, а также
  `C:\py` — примеры из книги, а не универсальные environment values.
- Рекомендации по Komodo Edit, Vim/Emacs plugins и historical Python/IDLE menu paths
  не проверялись на современную актуальность.

## Conditional artifacts

Раздел 6.6 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
