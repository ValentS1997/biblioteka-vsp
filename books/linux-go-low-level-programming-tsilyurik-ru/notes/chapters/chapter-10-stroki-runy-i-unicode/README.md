# Глава 10. Строки, руны и UNICODE

Статус: **RAG_GROUNDED**

## Scope

Глава посвящена обработке многоязычного текста в Go и строится от низкоуровневого представления строки к прикладным text-processing examples.

Основные темы:

1. `string`, bytes и `rune`;
2. `len(string)`, `[]rune` и `range`;
3. преобразование `string ↔ []rune`;
4. неизменяемость строк в формулировке источника;
5. `strings.Map`, `strings.ToLower`, `strings.ReplaceAll`;
6. поэтапная реализация palindrome checker;
7. `regexp`, raw string patterns и RE2-oriented syntax;
8. `FindAllString`, `FindAllStringIndex`, replacement functions;
9. обработка multilingual input через stdin/files.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Строки, руны и UNICODE`
- RAG chunk range: `p0223:c01` … `p0232:c01`
- Included chunks: **10**
- PDF page range: **223–232**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - TOC places `Строки, руны и UNICODE` at 223 and its sources at 232;
  - page 223 starts the chapter;
  - page 232 ends with its source list;
  - page 233 starts separate chapter `Элементы функционального программирования`.

## Main principle

Источник постоянно разделяет три уровня:

```text
string bytes
    ↓
rune/code-point-oriented processing
    ↓
library-level string/regexp transforms
```

Для non-ASCII text источник показывает, что byte indexing и `len(string)` дают byte-oriented representation, тогда как `range` и преобразование к `[]rune` используются для работы с многобайтными символами в модели главы.

## Chapter map

```text
string bytes / rune
      ↓
unicode/utf8
      ↓
strings.Map / transformations
      ↓
palindrome word checker
      ↓
phrase normalization
      ↓
regexp-based normalization
      ↓
regexp search / indexes / replace functions
```

## Palindrome progression

Глава намеренно развивает один пример по этапам:

1. `palindrow` — прямое сравнение `[]rune`;
2. `palindrob` — lower-case + removal of spaces;
3. `palindrom` — additional normalization через replacements и regexp.

Это полезно как пример iterative refinement: новый input class выявляет новый дефект нормализации, после чего код расширяется.

## Operational boundary

Read-only:

- `cat dig.txt` в pipeline;
- чтение заранее подготовленных input files.

Workload / compile-run:

- запуск локальных examples;
- `go run finddig.go` компилирует и запускает программу во временном workflow.

State-changing source edits/build commands внутри chapter boundary явно не показаны.

## Limitations

- Технические формулировки о UTF-8, internal memory placement strings и regexp capabilities сохраняются как source claims.
- Palindrome regexp на странице 228 имеет важную semantic limitation для Greek/non-Latin input; см. `source-findings.md`.
- Формулировка `\pL+` как «любой символ UNICODE» не подтверждается самой главой для произвольных Unicode categories.
- Никакая внешняя спецификация Go/Unicode/RE2 для исправления главы не использовалась.

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
