# Глава 3. Неформально о синтаксисе Go

Статус: **RAG_GROUNDED**

## Scope

Глава даёт неформальное введение в основные конструкции Go с постоянным сравнением с C/C++. Автор сознательно не строит полный справочник языка, а выбирает возможности, которые понадобятся дальше в книге.

Основные блоки:

1. синтаксис строк, точки с запятой, форматирование;
2. указатели, типизация, объявления и нулевые значения;
3. массивы, срезы, `new`, `make`, структуры и map;
4. управляющие конструкции и операции;
5. функции, множественные возвраты, variadic-функции, `defer`, функции высших порядков;
6. встроенные функции;
7. методы, embedding и интерфейсы;
8. обработка ошибок, `error`, `panic`, `recover`;
9. пакеты, import и область видимости;
10. примеры стандартной библиотеки: `fmt`, строки/Unicode, `math/big`, `testing`.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source format: PDF
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Неформально о синтаксисе Go`
- RAG chunk range: `p0066:c01` … `p0125:c01`
- Included chunks: **60**
- PDF page range: **66–125**
- Printed page range visible in extraction: **66–125**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 66 starts with `Неформально о синтаксисе Go`;
  - page 125 finishes the chapter source list;
  - page 126 starts `Новости от последних версий...`.

## Main principle

Источник объясняет Go через уменьшение синтаксической избыточности и строгие правила языка: меньше альтернативных конструкций, явные преобразования типов, отсутствие неиспользуемых переменных/import, встроенное форматирование, значения и методы вместо классической модели классов, неявная реализация интерфейсов и явная обработка ошибок через возвращаемые значения.

## Chapter map

```text
syntax / formatting
      ↓
types / declarations / conversions
      ↓
arrays / slices / structs / maps
      ↓
if / for / switch / operators
      ↓
functions / multiple returns / variadic / defer
      ↓
methods / embedding / interfaces
      ↓
error / panic / recover
      ↓
packages / imports / visibility
      ↓
fmt / strings / Unicode / math/big / testing
```

## Important source-grounded points

- Конец непустой строки может влиять на автоматическую постановку точки с запятой.
- `gofmt` / `go fmt` представлены как механизм единого стиля.
- Источник подчёркивает явные преобразования типов и строгую типизацию.
- Массивы и срезы рассматриваются как разные по семантике сущности; подробно обсуждаются `new`, `make`, `len`, `cap`, `append`.
- Для именованных типов могут определяться методы; receiver может быть значением или указателем.
- Интерфейс реализуется набором методов без отдельной декларации реализации.
- Ошибки описываются через тип `error` и множественный возврат; `panic/recover` выделяются для экстремальных ситуаций.
- Экспорт из пакета связывается с именами, начинающимися с большой буквы.
- В конце глава показывает отдельные stdlib-возможности и базовую схему `go test`.

## Limitations

- Это именно неформальное изложение; источник сам говорит, что часть языка опущена или затронута вскользь.
- Артефакты не обновляют синтаксис/семантику Go по современным внешним источникам.
- Формулировки, вызывающие сомнения, не исправляются из model memory.
- Обнаруженный внутренний code mismatch в примере `iota` вынесен в `source-findings.md`.

## Conditional artifacts

- explicit chapter-end summary: **not present**
- review questions/exercises: **not present**
- source finding: **present**

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
