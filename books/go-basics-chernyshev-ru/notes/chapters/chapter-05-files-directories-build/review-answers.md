# Ответы на вопросы для самопроверки — глава 5

Это RAG-grounded ответы по материалу главы. Они не являются официальным издательским ключом.

## 1. Файл и операции

Source описывает файл как byte-oriented persistent object. Показаны операции:
- create/open;
- inspect;
- read/write;
- rename/move;
- remove;
- existence check;
- copy;
- formatted read/write.

Основные APIs: `os.Create`, `os.Open`, `os.Stat`, `os.Rename`, `os.Remove`, `os.OpenFile`, `io.Copy`, `bufio.Scanner`.

Provenance: `p0213:c01–p0229:c01`.

## 2. Преимущества `OpenFile`

`os.OpenFile` — универсальный механизм, объединяющий создание/открытие с явным режимом доступа и permissions:

~~~go
OpenFile(name string, flag int, perm FileMode) (*File, error)
~~~

Через flags можно выбрать read/write/read-write, append, create, exclusive create, sync, truncate.

Provenance: `p0221:c01–p0224:c01`.

## 3. Режимы и permission bits

Основные mutually exclusive access modes:
- `O_RDONLY`;
- `O_WRONLY`;
- `O_RDWR`.

Дополнительные combinable flags:
- `O_APPEND`;
- `O_CREATE`;
- `O_EXCL`;
- `O_SYNC`;
- `O_TRUNC`.

Permission bits задают read/write/execute access для owner/group/others. Source приводит, например:
- `0644` — owner read/write, остальные read;
- `0755` — owner read/write/execute, остальные read/execute.

Provenance: `p0221:c01–p0223:c01`.

## 4. Форматированная запись/чтение

Это file I/O через functions package `fmt`, где values записываются/читаются по обычному или явно заданному format.

Write:
- `Fprint`;
- `Fprintf`;
- `Fprintln`.

Read:
- `Fscan`;
- `Fscanf`;
- `Fscanln`.

Chapter uses this when structured fields need predictable textual layout. Для `Fprintf` / `Fscanf` source подчёркивает необходимость согласованного format string.

Provenance: `p0225:c01–p0229:c01`.

## 5. Директория и операции

Directory — filesystem container for files/subdirectories. Chapter demonstrates:
- create/remove;
- temporary directory;
- recursive parent creation;
- list entries;
- current path/navigation;
- rename/move;
- existence check.

APIs include `os.Mkdir`, `os.MkdirTemp`, `os.MkdirAll`, `os.ReadDir`, `os.Rename`, `os.Stat`, `os.IsNotExist`, `filepath.Join`.

Provenance: `p0230:c01–p0238:c01`.

## 6. JSON и его структуры

JSON — text, language-independent data exchange format.

Source выделяет две базовые structures:
- object — unordered collection of key:value pairs;
- array/list — ordered sequence of values.

Object key is string. Value may be string, number, bool, null, object or array.

Provenance: `p0239:c01`.

## 7. Serialization

Serialization/encoding — преобразование data structure в формат, пригодный для хранения/передачи.

В Go chapter uses package `encoding/json`, прежде всего `json.Marshal` / `json.MarshalIndent`.

Provenance: `p0240:c01–p0241:c01`.

## 8. Serialization struct → JSON

Пример pattern:

~~~go
data, err := json.Marshal(actor)
// or
data, err := json.MarshalIndent(actor, "", "  ")
~~~

Полученный `[]byte` можно вывести как string или записать в file.

Provenance: `p0240:c01–p0241:c01`.

## 9. Deserialization

Deserialization/decoding — обратное преобразование: из stored/transferred representation восстановить structure/value.

Chapter uses `json.Unmarshal`.

Provenance: `p0240:c01`, `p0242:c01`.

## 10. JSON → struct

Source pattern:

~~~go
actor := &Actor{}
data, err := os.ReadFile("actor.json")
err = json.Unmarshal(data, actor)
~~~

Target передаётся через pointer, чтобы decoder мог заполнить fields.

Provenance: `p0242:c01`.

## 11. Struct tags

Struct tag — metadata string после field declaration. В JSON chapter она задаёт имя key и serialization options.

Examples:

~~~go
Name string `json:"name"`
Field string `json:"-"`
Field string `json:"field,omitempty"`
~~~

Uses:
- rename JSON key;
- ignore field;
- omit zero-value field.

Provenance: `p0244:c01–p0245:c01`.

## 12. Nested JSON

Нужно описать nested structure соответствующими Go structs/slices и затем использовать обычные `Marshal/Unmarshal`.

Movie example содержит nested `Actor`, `Genre`, `Review` structs and slices; chapter reads JSON into `Movie` and serializes it back.

Если schema заранее неизвестна, source допускает `map[string]any`, но для known schema предпочитает structs.

Provenance: `p0247:c01–p0249:c01`.

## 13. Сборка Go application и build flags

Basic command:

~~~bash
go build
~~~

Output name/path:

~~~bash
go build -o new-app.exe
~~~

Flags specifically highlighted by chapter:
- `-v` — build information;
- `-x` — internal commands;
- `-race` — race detector;
- `-ldflags` — linker/configuration options.

Provenance: `p0271:c01–p0273:c01`.

## 14. Configuration from compile time to runtime

Chapter demonstrates four approaches:

1. **Runtime CLI flags** through package `flag`:

~~~bash
go run main.go -int=33 -bool
~~~

2. **Compile-time variables** through linker flags:

~~~bash
go build -ldflags "-X main.Version=1.2.3 -X main.VersionType=test"
~~~

3. **Static embedded config**:

~~~go
//go:embed embed_config.json
var configData []byte
~~~

4. **`.env` file** parsed at application startup, optionally merged with OS environment values.

Source additionally notes that `.env` should not be treated as the safest secret storage and should be excluded from remote repository.

Provenance: `p0273:c01–p0280:c01`.
