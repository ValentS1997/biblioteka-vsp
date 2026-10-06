# Source findings — глава 18

## Finding 1 — auto_add_now vs auto_now_add

Classification: **[Source argument-name mismatch]**

Provenance:
- chunk: `e0028:c05`
- EPUB spine item: `28`
- locator: `OEBPS/Text/978544614112-25.xhtml`

Shown model code uses:

~~~python
date_added = models.DateTimeField(
    auto_now_add=True
)
~~~

Prose explains the argument as:

~~~text
auto_add_now=True
~~~

Names differ.

Adjudication: intended argument name `[Needs confirmation]`.

Policy action: code-oriented artifacts preserve shown code and record prose mismatch.

## Finding 2 — django-admin.py vs django-admin

Classification: **[Source command mismatch]**

Provenance:
- chunks: `e0028:c02`, `e0028:c04`

Main project setup uses:

~~~bash
django-admin startproject ll_project .
~~~

Exercise 18.1 says:

~~~text
django-admin.py startproject tg_project .
~~~

Command names differ.

Adjudication: intended exercise command `[Needs confirmation]`.

## Finding 3 — admin URL missing development-server port

Classification: **[Source URL mismatch]**

Provenance:
- chunks: `e0028:c03`, `e0028:c08`

Development server is shown at:

~~~text
http://127.0.0.1:8000/
http://localhost:8000/
~~~

Later Entry admin section says:

~~~text
http://localhost/admin/
~~~

without `:8000`.

Adjudication: intended URL `[Needs confirmation]`.

## Finding 4 — ForeignKey misspelled as ForeighKey

Classification: **[Source terminology typo]**

Provenance:
- chunk: `e0028:c09`

Model code and earlier prose use `ForeignKey`.

Later shell explanation says:

~~~text
ForeighKey
~~~

Policy action: preserve source typo as finding.

## Finding 5 — Django documentation version mismatch

Classification: **[Source documentation-version mismatch]**

Provenance:
- chunks: `e0028:c02`, `e0028:c05`, `e0028:c18`

Chapter setup/output references Django 4.1 and links Model Field Reference under `/en/4.1/`.

Exercise 18.7 points to template docs under:

~~~text
https://docs.djangoproject.com/en/2.2/ref/templates/
~~~

Versions differ.

Current appropriate docs version: `[Needs confirmation]`.

## Finding 6 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:
- affected starts observed: `e0028:c02`–`e0028:c18`
- EPUB spine item: `28`
- locator: `OEBPS/Text/978544614112-25.xhtml`

Observed starts include continuation fragments such as:
- `я виртуальной среды ll_env...`;
- `вок создается файл manage.py...`;
- `ает только запросы вашей системы...`;
- `обой обычный класс...`;
- `изменить базу данных...`;
- `rning_logs Django создает...`;
- `key) происходит...`;
- `сли вы щелкнете...`;
- `м, у вас есть модели Pizza...`;
- `jango вызывает index()...`;
- `рупных проектах...`;
- `тавит обновленный URL...`;
- and later continuation fragments through `e0028:c18`.

Cross-check:
- adjacent chunks preserve context;
- exercises 18.1–18.8 recoverable;
- chapter-end summary intact;
- `e0029:c01` confirms chapter 19;
- no chapter-level semantic loss detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

## Security/credential boundary

The chapter creates a superuser and discusses password hashing, but it does not define operational secret-management procedures for storing/administering credentials.

Real credentials must not be placed in chapter artifacts.
