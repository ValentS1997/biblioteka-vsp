# Chapter 14 — «Заключение»

Статус: **RAG_GROUNDED**

> Project numbering note: в исходном PDF заголовок `Заключение` не имеет номера. Номер **14** используется только для последовательности chapter artifacts после главы 13.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source heading: `Заключение`
- Source heading numbered: **no**
- Project artifact number: **14**
- PDF page: **280**
- RAG chunk: `p0280:c01`
- Included chunks: **1**
- Boundary verified: **yes**
- Page 281 starts `Об авторе` and is excluded.
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`

## Scope

Заключение возвращает книгу к её главной теме: не синтаксис Go как таковой, а эффективное использование многопроцессорного hardware.

Автор сводит книгу к трём утверждениям:

1. в Go остаётся много нерассмотренных возможностей;
2. центральная задача книги — использование множества процессоров одновременно;
3. рост производительности систем всё сильнее связывается с ростом числа processors, а не только clock frequency.

## Canonical takeaway

```text
hardware trend
→ more processors
→ software must expose useful parallelism
→ Go is presented by the author as a tool designed for this reality
```

При этом практические главы книги уже показали важное ограничение: многопроцессорность полезна только при корректной декомпозиции, контроле shared state и приемлемом synchronization overhead.

## Conditional artifacts

- explicit concluding summary: **present**
- review questions/exercises: **not present**
- shell commands: **not present**
- source findings: **present**

## Artifacts

- [summary.md](./summary.md)
- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
