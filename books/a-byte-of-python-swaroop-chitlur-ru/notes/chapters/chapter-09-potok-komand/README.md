# Глава 9. Поток команд

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 9 — «Поток команд». Она показывает, как изменить последовательное выполнение
программы с помощью условий и циклов: `if`, `while`, `for`, а также `break`
и `continue`.

Разделы, подтверждённые RAG:

- 9.1 Оператор if
- 9.2 Оператор while
- 9.3 Цикл for
- 9.4 Оператор break
  - 9.4.1 Поэтический Python Swaroop’а
- 9.5 Оператор continue
- 9.6 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0059:c01` — `p0066:c01`
- PDF pages: 59–66
- printed pages visible in chapter: 51–58
- chapter start: PDF page 59, heading «Поток команд»
- chapter end: PDF page 66, section 9.6 «Резюме»
- next chapter boundary: PDF page 67 begins «Функции»
- boundary verified: yes

## Main principle

Поток выполнения больше не обязан идти строго сверху вниз:

- `if` выбирает один из ветвей выполнения по условию;
- `while` повторяет block, пока условие истинно;
- `for` итерирует по последовательности;
- `break` досрочно завершает loop и подавляет соответствующий loop-`else`;
- `continue` пропускает оставшуюся часть текущей итерации.

## Chapter map

| Section | Source-grounded concept |
|---|---|
| 9.1 | `if / elif / else`, nested `if`, обязательное двоеточие и indentation blocks. |
| 9.2 | `while` повторяет block до ложного condition; optional `else` выполняется при нормальном завершении цикла. |
| 9.3 | `for ... in` проходит по элементам sequence; `range()` формирует значения для iteration. |
| 9.4 | `break` немедленно прекращает `for` или `while`; loop-`else` после `break` не выполняется. |
| 9.4.1 | Поэтический текст используется как sample input для `break.py`. |
| 9.5 | `continue` пропускает оставшиеся statements текущего loop block и переходит к next iteration. |
| 9.6 | `if`, `while`, `for`, `break`, `continue` названы основными flow-control constructs. |

## Core examples

### if.py

```python
number = 23
guess = int(input('Введите целое число : '))

if guess == number:
    print('Поздравляю, вы угадали,')
elif guess < number:
    print('Нет, загаданное число немного больше этого.')
else:
    print('Нет, загаданное число немного меньше этого.')

print('Завершено')
```

### while.py

Source uses a Boolean flag:

```python
running = True
while running:
    ...
    if guess == number:
        running = False
else:
    print('Цикл while закончен.')
```

### for.py

```python
for i in range(1, 5):
    print(i)
else:
    print('Цикл for закончен')
```

### break.py

```python
while True:
    s = input('Введите что-нибудь : ')
    if s == 'выход':
        break
    print('Длина строки: ', len(s))
```

### continue.py

```python
while True:
    s = input('Введите что-нибудь : ')
    if s == 'выход':
        break
    if len(s) < 3:
        print('Слишком мало')
        continue
    print('Введённая строка достаточной длины')
```

## Operational acceptance

После главы читатель должен уметь:

- построить `if / elif / else` branch;
- объяснить роль `:` и indentation после control statement;
- использовать `while` с condition и optional `else`;
- использовать `for ... in range(...)`;
- объяснить, когда loop-`else` выполняется и когда подавляется `break`;
- использовать `continue` для пропуска остатка текущей итерации.

## Safety boundary

- Примеры `while True` могут выполняться неопределённо долго, пока пользователь не
  введёт source sentinel `выход`; это workload-generating behavior.
- Все команды запускают учебные programs и принимают интерактивный input; системные
  настройки/пакеты глава не изменяет.
- Сохранение `if.py`, `while.py`, `for.py`, `break.py`, `continue.py` изменяет
  filesystem state; source rollback для файлов не задан.
- Source command examples используют `python ...`, а не `python3 ...`; не
  нормализовать их молча.

## Conditional artifacts

Раздел 9.6 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Review/control questions в границе главы отсутствуют, поэтому
`review-questions.md` и `review-answers.md` не создаются.
