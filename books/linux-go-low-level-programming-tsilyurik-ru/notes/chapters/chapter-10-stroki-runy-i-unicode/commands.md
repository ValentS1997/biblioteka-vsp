# Commands — глава 10 «Строки, руны и UNICODE»

Только команды, подтверждённые RAG страниц 223–232.

| Command | Class | Purpose |
|---|---|---|
| `./rune_len` | workload | Сравнить byte/rune-oriented representation |
| `./rune_out` | workload | Показать `[]rune`, code values и conversion back to string |
| `./map` | interactive workload | Проверить `strings.Map` transformation |
| `./palindrow` | interactive workload | Word palindrome checker |
| `./palindrow words.txt` | read-file workload | Проверка набора слов |
| `./palindrow worde.txt` | negative test | Проверка file-open error path |
| `./palindrob` | interactive workload | Lower-case/space-normalized checker |
| `./palindrob palindrom.txt` | read-file workload | Phrase test before regexp normalization |
| `./palindrom palindrom.txt` | read-file workload | Regexp-normalized phrase test |
| `go run finddig.go` | compile-run workload | Interactive regexp digit extraction |
| `go run finddig.go < dig.txt` | compile-run/read-file | Batch regexp test |
| `cat dig.txt \| go run finddig.go` | read + compile-run | Equivalent pipeline input path |
| `./replw` | interactive workload | Word extraction + replacement callback |
| `./replw < wrd.txt` | read-file workload | Batch multilingual regexp test |

## State-changing commands

Explicit persistent build commands are not shown inside this chapter.

`go run` performs compilation/execution, but the source does not describe a persistent build artifact for these invocations.

```text
persistent build command: [Needs confirmation]
cleanup command: [Needs confirmation]
```

## Verification focus

### rune examples

Check:

- byte count;
- rune/code-point count as represented by source;
- displayed byte sequence;
- `range` positions.

### palindrome examples

Do not verify only `true/false`.

Also verify the normalization input after:

- `ToLower`;
- space removal;
- selected letter replacements;
- regexp filtering.

This is necessary because page 228 can reduce unsupported scripts to empty/partial input while still producing `true`.

### regexp examples

For `finddig.go`, source checks:

- matched numeric strings;
- byte indexes;
- index→value map.

For `replw`, source checks:

- number of matched words;
- callback invocation;
- transformed lowercase output.

## Risk

No system configuration changes are evidenced.

Risks are primarily semantic:

- accidental byte-oriented processing of multilingual text;
- regex that excludes scripts/categories not represented in the pattern;
- false-positive normalization results.
