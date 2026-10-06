# Глава 2. Разворачиваем экосистему Go

Статус: **RAG_GROUNDED**

## Scope

Глава посвящена практическому развёртыванию и исследованию Go toolchain в Linux. Автор последовательно проходит:

1. установку GoLang и gccgo из пакетных репозиториев;
2. сосуществование и переключение нескольких версий Go;
3. сборку GoLang из исходного Git-дерева;
4. проверку toolchain на первой программе;
5. статическую/динамическую компоновку и выбор компилятора;
6. встроенную справочную систему `go help`;
7. переменные среды Go;
8. GOPATH, GOTOOLDIR, GOARCH и GOOS;
9. кросс-компиляцию;
10. форматирование, `build`, `clean`, `run`, `get`, `tool`;
11. низкоуровневые утилиты `compile`, `link`, `objdump`;
12. Cgo;
13. дополнительный инструментарий и Delve.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source format: PDF
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Разворачиваем экосистему Go`
- RAG chunk range: `p0026:c01` … `p0065:c01`
- Included chunks: **40**
- PDF page range: **26–65**
- Printed page range visible in extraction: **26–65**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 26 starts with `Разворачиваем экосистему Go`;
  - page 65 ends with the chapter sources;
  - page 66 starts `Неформально о синтаксисе Go`.

## Main principle

Главная практическая идея главы: Go — это не только компилятор, а целая управляемая toolchain-экосистема. Перед изменениями автор постоянно показывает диагностику: найти пакет, проверить бинарник, зафиксировать версию, увидеть effective environment, проверить формат/зависимости результата. После этого выполняется изменение — установка, сборка, переключение версии или компиляция — и затем повторная проверка.

## Operational map

```text
repository/package search
        ↓
install toolchain
        ↓
which / version
        ↓
optional: alternatives / source build
        ↓
hello.go → build/run → file/ldd
        ↓
go help / go env
        ↓
GOPATH / GOTOOLDIR
        ↓
GOOS + GOARCH → cross-build
        ↓
fmt / build / clean / run / get / tool
        ↓
compile/link/objdump + Cgo
        ↓
Delve / auxiliary tooling
```

## Important boundaries

- Версии пакетов и пути в листингах принадлежат окружению автора; книга сама предупреждает, что они могут отличаться.
- Команды с `sudo apt install`, `update-alternatives`, `go fmt`, `go clean`, `go get`, `go install`, `git clone`, `git fetch`, `export` изменяют состояние или рабочее окружение.
- `GOOS`/`GOARCH` в примерах используются для кросс-сборки; проверка результата делается через `file` и фактический запуск на целевой системе.
- `go env` и `go help` — ключевые read-only источники информации именно для установленной версии Go.
- Часть материала описывает legacy GOPATH/get workflow; артефакты не обновляют его из внешних источников.

## Conditional artifacts

- explicit chapter-end summary: **not present**
- review questions/exercises: **not present**
- source finding: **present**, см. `source-findings.md`

## Artifacts

- [cheatsheet.md](./cheatsheet.md)
- [commands.md](./commands.md)
- [diagram.md](./diagram.md)
- [visual-cheatsheet.svg](./visual-cheatsheet.svg)
- [visual-cheatsheet-detailed.svg](./visual-cheatsheet-detailed.svg)
- [source-findings.md](./source-findings.md)
