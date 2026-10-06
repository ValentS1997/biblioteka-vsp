# Глава 19. Что дальше

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 19 — «Что дальше». Это финальная основная глава книги. Она предлагает две
самостоятельные задачи и перечисляет направления дальнейшего развития после базового
изучения Python: упражнения, чтение чужого кода, Q&A, учебники, видео, обсуждения,
новости, установка библиотек, GUI toolkits, альтернативные реализации Python и
functional programming.

Разделы, подтверждённые RAG:

- вводная часть + задача «Адресная книга»
- задача `replace`
- 19.1 Упражнения
- 19.2 Примеры программ
- 19.3 Вопросы и ответы
- 19.4 Советы и рекомендации
- 19.5 Учебники
- 19.6 Видео
- 19.7 Обсуждение
- 19.8 Новости
- 19.9 Установка библиотек
- 19.10 Графические программы
- 19.11 Резюме по инструментам ГИП
- 19.12 Различные реализации
- 19.13 Функциональное программирование
- 19.14 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0145:c01` — `p0150:c01`
- PDF pages: 145–150
- printed pages visible in chapter: 137–142
- chapter start: PDF page 145, heading «Что дальше»
- chapter end: PDF page 150, section 19.14 «Резюме»
- next boundary: PDF page 151 begins «Приложение: FLOSS»
- boundary verified: yes

## Main principle

После базового курса source переводит читателя из режима «изучать конструкции языка»
в режим самостоятельной практики:

1. написать собственную программу;
2. решать упражнения;
3. читать чужой код;
4. использовать community/documentation resources;
5. подключать external libraries;
6. выбрать GUI toolkit при необходимости;
7. знать о других Python implementations;
8. расширять programming paradigm knowledge.

## Core tasks

### Address book

Source asks for a command-line address-book application that can:

- browse contacts;
- add contacts;
- modify contacts;
- delete contacts;
- search contacts;
- persist contact data to disk.

Source hint:

- create a class for personal/contact data;
- store contact-card objects in a dictionary;
- use contact names as keys;
- use `pickle` for persistent storage;
- use dictionary methods for add/change/delete operations.

No implementation is supplied.

### replace command

Source asks to implement a command called `replace` that replaces one string with
another in a list of supplied files.

The task may range from simple literal replacement to pattern/regular-expression search.

No CLI syntax, algorithm, backup procedure or implementation is supplied.

## Further-study map

| Section | Source-grounded direction |
|---|---|
| 19.1 | Python exercises; Stack Overflow discussion named by source. |
| 19.2 | Read/write many programs; PLEAC, Rosetta Code, java2s, Python Cookbook, Module of the Week. |
| 19.3 | Official FAQ/do-and-don't material, Norvig questions, interview questions, Stack Overflow. |
| 19.4 | Python tricks/tips and David Mertz article series. |
| 19.5 | Awaretek tutorial list. |
| 19.6 | PyVideo. |
| 19.7 | python-tutor mailing list after doing own homework first. |
| 19.8 | official Planet Python. |
| 19.9 | Python package catalog and `pip`. |
| 19.10 | Kivy, PyGTK, PyQt, wxPython as GUI options in source. |
| 19.11 | Choose GUI toolkit by cost/licensing, target platforms and desktop environment. |
| 19.12 | CPython, Jython, IronPython, PyPy, Stackless Python, CLPython, IronMonkey. |
| 19.13 | Functional-programming resources. |
| 19.14 | End of the book; reader is encouraged to automate/build independently. |

## Operational acceptance

После главы читатель должен уметь:

- сформулировать собственный project scope;
- разложить address-book task на data model, dictionary operations and persistence;
- распознать, что `replace` является file-modifying task;
- понимать source recommendation искать готовые libraries before reinventing functionality;
- знать source categories дальнейшего обучения;
- объяснить, что CPython — только одна из перечисленных source implementations;
- отличить OOP direction от упомянутого functional-programming direction.

## Safety / integrity boundary

### Address book

Persistent storage through `pickle` implies filesystem writes.

Actual storage path, overwrite/update behavior and rollback:
**[Needs confirmation]** because source provides no implementation.

### replace

A working replacement utility would modify input files.

Before any real implementation/run would require:

- exact input paths;
- match/replace semantics;
- encoding;
- backup/atomic-write behavior;
- rollback strategy.

All are **[Needs confirmation]**.

### External resources

This workflow is `rag_only`. Named websites, projects, licenses, package-management
details and platform claims are preserved as source references/historical statements.
Their current availability/status is not verified here.

## Conditional artifacts

Раздел 19.14 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Formal review/control questions отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
