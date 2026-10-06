# Глава 7. Основы

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 7 — «Основы». Она вводит базовые элементы Python, необходимые перед переходом
к операторам и управляющим конструкциям: комментарии, литеральные константы,
числа, строки, форматирование, переменные, идентификаторы, типы данных, объекты,
логические/физические строки и отступы.

Разделы, подтверждённые RAG:

- 7.1 Комментарии
- 7.2 Литеральные константы
- 7.3 Числа
- 7.4 Строки
  - 7.4.1 Одинарные кавычки
  - 7.4.2 Двойные кавычки
  - 7.4.3 Тройные кавычки
  - 7.4.4 Строки неизменяемы
  - 7.4.5 Объединение строковых констант
  - 7.4.6 Метод format
- 7.5 Переменные
- 7.6 Имена идентификаторов
- 7.7 Типы данных
- 7.8 Объекты
  - 7.8.1 Пример: Использование переменных и констант
- 7.9 Логические и физические строки
- 7.10 Отступы
- 7.11 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0043:c01` — `p0052:c01`
- PDF pages: 43–52
- printed pages visible in chapter: 35–44
- chapter start: PDF page 43, heading «Основы»
- chapter end: PDF page 52, section 7.11 «Резюме»
- next chapter boundary: PDF page 53 begins «Операторы и выражения»
- boundary verified: yes

## Main principle

Глава формирует базовую модель программы на Python:

- значения задаются литеральными константами;
- переменные связывают имена со значениями;
- строки — неизменяемые последовательности символов;
- идентификаторы подчиняются правилам именования и чувствительны к регистру;
- Python рассматривает значения и функции как объекты;
- одна логическая строка обычно соответствует одной физической строке;
- блоки программы определяются отступами.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 7.1 | Комментарии должны помогать объяснять «почему», а не только «как». |
| 7.2 | Литеральные константы используются буквально и не меняют собственного значения. |
| 7.3 | Числа: целые, floating-point, complex; отдельного `long int` источник не выделяет. |
| 7.4 | Строки как Unicode sequences; single/double/triple quotes, immutability, adjacent-literal concatenation. |
| 7.4.6 | `str.format()`: positional placeholders, implicit positions, precision/alignment and keyword placeholders. |
| 7.5 | Переменные — именованные области/ссылки для хранения информации, значение может меняться. |
| 7.6 | Правила identifier names и case sensitivity. |
| 7.7 | Переменные могут хранить значения разных типов; custom types позже создаются через classes. |
| 7.8 | Всё в Python source-framing рассматривается как объект, включая числа, строки и функции. |
| 7.8.1 | Assignment и повторное присваивание на примере `var.py`. |
| 7.9 | Различие logical/physical lines; semicolon, explicit `\` continuation и implicit continuation inside brackets. |
| 7.10 | Leading whitespace формирует blocks; неправильный indent приводит к `IndentationError`. |
| 7.11 | Перед control-flow нужно освоить перечисленные базовые детали. |

## Core examples

### Variables

```python
i = 5
print(i)
i = i + 1
print(i)
```

Source output:

```text
5
6
```

### format

```python
age = 26
name = 'Swaroop'

print('Возраст {0} -- {1} лет.'.format(name, age))
print('Почему {0} забавляется с этим Python?'.format(name))
```

### Indentation failure

Source example deliberately begins one line with an extra space and shows:

```text
IndentationError: unexpected indent
```

## Operational acceptance

После главы читатель должен уметь:

- отличить literal constant от variable;
- выбрать допустимое identifier name;
- объяснить immutability строк;
- использовать source examples метода `format()`;
- понимать assignment `=` в `var.py`;
- различать logical и physical lines;
- объяснить, почему indentation является частью структуры Python code;
- распознать `IndentationError` из source example.

## Limitations

- В первых comment examples на PDF page 43 в RAG отсутствует закрывающая quote внутри
  `print('Привет, Мир!)`; это сохранено как source finding, а не исправлено молча.
- В RAG есть extraction glyph `StackOverﬂow`.
- Source execution examples используют и `python`, и стандартную процедуру
  `python3 program.py`; это сохранено как source mismatch.
- Современные style recommendations, Python-version differences и current tooling
  внешне не проверялись.

## Conditional artifacts

Раздел 7.11 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
