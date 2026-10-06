# Глава 8. Осваиваемся в синтаксисе Go

Статус: **RAG_GROUNDED**

## Scope

Глава закрепляет ранее рассмотренный синтаксис Go на наборе небольших прикладных задач.

Основные примеры:

1. CLI-утилита `echo` и пакет `flag`;
2. итерационный квадратный корень — сравнение C/Go;
3. вычисление π с `math/big`;
4. вычисления произвольной точности;
5. среднее/дисперсия/СКО случайной последовательности;
6. параметры выпуклого 2D-многоугольника;
7. TCP echo server/client;
8. многоклиентский TCP server с goroutine;
9. минимальный HTTP server;
10. порядок итерации `map`.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Осваиваемся в синтаксисе Go`
- RAG chunk range: `p0197:c01` … `p0215:c01`
- Included chunks: **19**
- PDF page range: **197–215**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 197 starts with `Осваиваемся в синтаксисе Go`;
  - page 215 contains the chapter source list;
  - page 216 starts `Структуры данных, типы и их методы`.

## Main principle

Глава не вводит отдельную новую языковую подсистему. Она показывает, как уже рассмотренные конструкции Go комбинируются в небольших законченных программах: CLI parsing, numeric algorithms, arbitrary precision, structures/methods, networking, goroutines and maps.

## Example map

```text
flag / CLI
   ↓
numeric iteration
   ↓
math/big
   ↓
streaming statistics
   ↓
structs + methods + complex numbers
   ↓
TCP server/client
   ↓
goroutine-per-connection
   ↓
net/http
   ↓
map iteration behavior
```

## Operational boundary

Read-only / observation:

- `ls -l`;
- existing binary execution when no external side effects are expected;
- terminal client observation.

State-changing:

- `go build`;
- `make`;
- build outputs in current directory.

Network/listening workloads:

- TCP server on ports `51500` / `51501`;
- clients `nc`, `socat`, `telnet`;
- HTTP server on `localhost:4000`.

These examples should not be copied to a production host without checking port ownership, bind address, firewall policy and process lifecycle.

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
