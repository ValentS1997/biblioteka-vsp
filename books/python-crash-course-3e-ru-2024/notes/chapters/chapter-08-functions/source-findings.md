# Source findings — глава 8

## Finding 1 — default для age: code vs explanation

Classification: **[Source code/text mismatch]**

Provenance:

- chunk: `e0017:c07`
- EPUB spine item: `17`
- locator: `OEBPS/Text/978544614112-14.xhtml`

Source code defines:

~~~python
def build_person(first_name, last_name, age=''):
~~~

Но пояснение непосредственно после примера утверждает, что параметру `age` назначено специальное default value `None`.

Эти две source variants расходятся.

Adjudication: `[Needs confirmation]`.

Policy action: не заменять `''` на `None` и не выбирать один вариант как правильный вне конкретного упражнения.

## Finding 2 — indentation в while example

Classification: **[Source code/text mismatch]** с возможной extraction-origin.

Provenance:

- chunk: `e0017:c08`
- EPUB spine item: `17`
- locator: `OEBPS/Text/978544614112-14.xhtml`

В извлечённом коде после:

~~~python
if l_name == 'q':
    break
~~~

строки:

~~~python
formatted_name = get_formatted_name(f_name, l_name)
print(f"\nHello, {formatted_name}!")
~~~

идут без indentation относительно `while True`.

Однако surrounding explanation и показанный interaction демонстрируют приветствие после каждой введённой пары name/surname до следующего прохода цикла.

Adjudication: точная причина — ошибка исходной разметки или потеря indentation при extraction — `[Needs confirmation]`.

Policy action: не исправлять canonical RAG. В instructional artifacts описывать intended control-flow по surrounding source, а finding сохранять явно.

## Finding 3 — chunk-boundary clipping / overlap

Classification: **[Source extraction issue]**

Provenance:

- affected starts observed: `e0017:c02`–`e0017:c16`
- EPUB spine item: `17`
- locator: `OEBPS/Text/978544614112-14.xhtml`

Observed starts include partial continuations such as `ого имени...`, `ва describe_pet...`, `ние по умолчанию...`, `тат...`, `отформатированное...`, `middle_name...`, `тированное...`, `имен передается...`, `pleted_models...`, `nted_designs...`, `тов...` and other continuation fragments.

Cross-check:

- adjacent preceding chunks preserve the relevant context;
- exercises 8.1–8.17 remain recoverable;
- chapter-end summary is intact;
- `e0018:c01` confirms chapter 9;
- no chapter-level semantic loss was detected.

Adjudication: extractor/chunker root cause `[Needs confirmation]`.

Policy action: keep legacy RAG unchanged until a separately justified controlled rebuild.
