# Source findings — глава 4 «Новости от последних версий...»

## Finding 1 — module name mismatch after go mod init

Classification: **[Source code/output mismatch]**

Provenance:

- PDF/RAG page 126, chunk `p0126:c01`;
- continuation page 127, chunk `p0127:c01`.

Observed sequence:

```bash
go mod init generic
```

Источник сообщает создание модуля `generic`, но сразу после этого первый показанный `cat go.mod` содержит:

```text
module types
go 1.20
```

На следующей странице другой вывод `cat go.mod` уже содержит:

```text
module generic
go 1.20
...
```

Impact:

Первый показанный `module types` не согласуется с командой `go mod init generic` и последующим листингом.

Action:

- несоответствие не исправлялось молча;
- в operational artifacts команда сохранена как `go mod init generic`;
- canonical interpretation первого `module types`: **[Needs confirmation]**.

## Finding 2 — build output name vs executed filename

Classification: **[Source code/output mismatch]**

Provenance:

- PDF/RAG page 128, chunk `p0128:c01`.

Observed:

Build command:

```bash
go build -o print_slice print_slice.0.go
```

Но последующий запуск показан как:

```bash
./print_slice.0
```

Impact:

`-o print_slice` и `./print_slice.0` обозначают разные output filenames.

Action:

- обе строки сохранены как source evidence;
- в `commands.md` verification для этой конкретной пары помечен как source mismatch;
- правильное имя без внешней проверки: **[Needs confirmation]**.
