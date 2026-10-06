# Глава 4. Новости от последних версий...

Статус: **RAG_GROUNDED**

## Scope

Глава вынесена отдельно от предыдущего синтаксического обзора и рассматривает две возможности, появившиеся в более поздних версиях Go относительно основной части книги:

1. **Modules** — управление модулем и зависимостями через `go.mod`, `go.sum`, `go mod init`, `go get`, `go mod tidy`;
2. **Generics** — параметризованные функции и типы, type inference и constraints.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Новости от последних версий...`
- RAG chunk range: `p0126:c01` … `p0131:c01`
- Included chunks: **6**
- PDF page range: **126–131**
- Printed page range visible in extraction: **126–131**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 126 starts with `Новости от последних версий...`;
  - page 131 ends with chapter sources;
  - page 132 starts `Часть 2. Конкурентность и многопроцессорность`.

## Main principle

Глава показывает переход от ранней Go-модели к двум более новым механизмам: явному модульному управлению зависимостями и параметризованному коду. Автор подчёркивает динамичность этих возможностей и не пытается дать исчерпывающее описание.

## Modules flow

```text
go mod init
    ↓
go.mod
    ↓
imports require external module
    ↓
go get <module>
or
go mod tidy
    ↓
go.mod + go.sum + module cache
    ↓
go build
```

## Generics flow

```text
func PrintSlice[T any](s []T)
        ↓
explicit type args: PrintSlice[string](...)
        ↓
type inference: PrintSlice(...)
        ↓
constraints
        ↓
comparable / custom interface / constraints.Ordered
```

## Important boundaries

- Глава прямо предупреждает, что описываемые возможности находились в развитии.
- Артефакты не обновляют modules/generics по внешней документации.
- Версии модулей и пути cache относятся к окружению автора.
- `go get`, `go mod tidy`, `go fmt`, `go build` меняют состояние проекта или локального cache.
- Найденные несоответствия в именах модуля и build artifact вынесены в `source-findings.md`.

## Conditional artifacts

- explicit chapter-end summary: **not present**
- review questions/exercises: **not present**
- source findings: **present**

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
