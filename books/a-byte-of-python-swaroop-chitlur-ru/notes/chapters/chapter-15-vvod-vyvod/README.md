# Глава 15. Ввод-вывод

Status: `RAG_GROUNDED`

Book: `a-byte-of-python-swaroop-chitlur-ru`

## Scope

Глава 15 — «Ввод-вывод». Она объединяет три source-направления I/O:

- взаимодействие с пользователем через `input()` / `print()`;
- чтение и запись файлов через `open()`, `write()`, `readline()`, `close()`;
- длительное хранение Python-объектов через модуль `pickle`.

Разделы, подтверждённые RAG:

- 15.1 Ввод от пользователя
- 15.2 Файлы
- 15.3 Pickle
- 15.4 Резюме

## Provenance

- source format: PDF
- source SHA-256: `ac1abb7761fccb914988a583b4362c1760bafc3489c34f3f1fdb4ba45a0d7db5`
- RAG chunks: `p0121:c01` — `p0126:c01`
- substantive content: PDF pages 121–125
- PDF page 126: only running footer for chapter 15
- printed pages visible in substantive content: 113–117
- chapter start: PDF page 121, heading «Ввод-вывод»
- chapter summary: PDF page 125, section 15.4 «Резюме»
- next chapter boundary: PDF page 127 begins «Исключения»
- boundary verified: yes

## Main principle

Программа должна уметь получать данные, выводить результаты и сохранять состояние.

Source progression:

`user input/output → text files → binary serialization with pickle`

## Chapter map

| Section | Source-grounded concept |
|---|---|
| Intro | `input()`, `print()`, string formatting/alignment methods such as `rjust`, and files as a common I/O form. |
| 15.1 | Read text from user; reverse with `[::-1]`; test palindrome; homework asks to ignore punctuation, spaces and letter case. |
| 15.2 | `open()`, read/write/append modes, text/binary mode, `write`, `readline`, `close`, EOF via empty string. |
| 15.3 | `pickle.dump` writes an object to binary file; `pickle.load` restores it. |
| 15.4 | Summary of I/O, files and `pickle`; next topic is exceptions. |

## Core examples

### user_input.py

```python
def reverse(text):
    return text[::-1]

def is_palindrome(text):
    return text == reverse(text)

something = input('Введите текст: ')
if (is_palindrome(something)):
    print("Да, это палиндром")
else:
    print("Нет, это не палиндром")
```

Source examples:

- `сэр` → not palindrome;
- `мадам` → palindrome;
- `топот` → palindrome.

### using_file.py

```python
poem = '''\
Программировать весело.
Если работа скучна,
Чтобы придать ей весёлый тон -
    используй Python!
'''

f = open('poem.txt', 'w')
f.write(poem)
f.close()

f = open('poem.txt')
while True:
    line = f.readline()
    if len(line) == 0:
        break
    print(line, end='')

f.close()
```

### pickling.py

```python
import pickle

shoplistfile = 'shoplist.data'
shoplist = ['яблоки', 'манго', 'морковь']

f = open(shoplistfile, 'wb')
pickle.dump(shoplist, f)
f.close()

del shoplist

f = open(shoplistfile, 'rb')
storedlist = pickle.load(f)
print(storedlist)
```

## Operational acceptance

После главы читатель должен уметь:

- получить строку через `input()`;
- применить source palindrome check через reverse slice;
- открыть file для read/write;
- объяснить source modes `r/w/a` и `t/b`;
- записать строку через `write`;
- читать по одной строке через `readline`;
- распознать EOF по empty string в source example;
- закрыть file через `close`;
- сохранить объект через `pickle.dump`;
- восстановить объект через `pickle.load`.

## Safety / integrity boundary

State-changing operations:

- `open('poem.txt', 'w')` + `write` создаёт/перезаписывает `poem.txt`;
- `open('shoplist.data', 'wb')` + `pickle.dump` создаёт/перезаписывает binary file;
- `del shoplist` меняет runtime namespace only.

Source rollback для созданных/перезаписанных файлов не задан: **[Needs confirmation]**.

Не добавляются:

- synthetic shell commands для просмотра/удаления files;
- external corrections к file/pickle semantics;
- отсутствующий URL из homework hint.

## Conditional artifacts

Раздел 15.4 — явное chapter-end «Резюме», поэтому создан `summary.md`.

Homework присутствует в 15.1, но это не formal review/control-question section; поэтому
`review-questions.md` и `review-answers.md` не создаются.
