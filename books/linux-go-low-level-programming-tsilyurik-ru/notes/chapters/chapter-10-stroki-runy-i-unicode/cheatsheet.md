# Cheatsheet — глава 10 «Строки, руны и UNICODE»

## Problem framing

Нужно обрабатывать multilingual UTF-8 text так, чтобы не путать:

- bytes;
- rune/code-point-oriented iteration;
- string-level transformations.

## 1. Bytes vs rune

Source example:

```go
fmt.Println(len(s))
fmt.Println(len([]rune(s)))

for i := 0; i < len(s); i++ {
    fmt.Printf("%02X", s[i])
}

for p, c := range s {
    fmt.Printf("%d:%q", p, c)
}
```

Source interpretation:

- `len(string)` — byte count;
- index `s[i]` — byte-oriented;
- `range` yields positions of encoded characters and rune values;
- `len([]rune(s))` is used by author as character count for examples.

## 2. string ↔ []rune

```go
r := []rune(j)
fmt.Println(string(r))
```

Источник показывает `unicode/utf8.RuneCountInString` как отдельный способ count.

## 3. String transformation

Пример circular digit transformation:

```go
strings.Map(func(r rune) rune {
    if unicode.IsNumber(r) {
        return '0' + (r-'0'+1)%10
    }
    return r
}, scanner.Text())
```

Source lesson: library functions can process a string through rune-oriented callback logic and return a transformed string.

## 4. Palindrome checker

### Stage A — direct rune comparison

```go
rstr := []rune(ustr)
for i := 0; i < len(rstr)/2; i++ {
    pali = rstr[i] == rstr[len(rstr)-i-1]
}
```

Input:

- stdin if no filename is supplied;
- file through `os.Open` otherwise.

### Stage B — normalize case and spaces

```go
rstr := []rune(
    strings.ReplaceAll(
        strings.ToLower(ustr), " ", ""))
```

### Stage C — additional replacements + regexp

Source example normalizes selected Cyrillic pairs and filters input via:

```go
var nonAlphaNum = regexp.MustCompile(`[^a-zа-я0-9 ]+`)
```

Important: this pattern does not establish general Unicode palindrome normalization. See source finding for Greek input.

## 5. regexp workflow

Pattern compilation:

```go
re, _ := regexp.Compile(`\d+`)
```

Search:

```go
re.FindAllString(s, -1)
re.FindAllStringIndex(s, -1)
```

Transformation:

```go
re.ReplaceAllStringFunc(s, rep2up)
```

Source recommends raw string literals for regexp patterns to reduce escape handling.

## 6. Multilingual word example

The source experiments with variants including:

```text
\w+
([Ё-Яa-ё]|[a-zA-Z])+
\S+
\pL+
```

Canonical artifact does not select a universally correct pattern from these examples; exact Unicode regexp semantics remain source-scoped.

## Verification

```bash
./rune_len
./rune_out
./map

./palindrow
./palindrow words.txt
./palindrob palindrom.txt
./palindrom palindrom.txt

go run finddig.go
go run finddig.go < dig.txt
cat dig.txt | go run finddig.go

./replw
./replw < wrd.txt
```

## Acceptance pattern

A text-processing example is considered verified when:

1. byte/rune counts match the demonstrated input;
2. multilingual input is not accidentally processed as independent UTF-8 bytes where rune processing is intended;
3. normalization rules are explicit;
4. regexp behavior is verified on representative scripts/categories;
5. success is not inferred only from a boolean result when normalization may have removed all meaningful input.

## Next action

Следующая глава — отдельная глава 11 `Элементы функционального программирования`.
