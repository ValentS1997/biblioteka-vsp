# Глава 9. Структуры данных, типы и их методы

Статус: **RAG_GROUNDED**

## Scope

Глава возвращается к уже знакомым типам Go и рассматривает их через семантику передачи значений и конкретные примеры.

Основные темы:

1. C-массивы как исходная точка сравнения;
2. Go arrays как значения фиксированного типа/размера;
3. pointer-to-array для намеренного изменения массива;
4. slices как отдельный тип;
5. многомерные и нерегулярные slices;
6. функции с множественным возвратом;
7. именованные return values и blank identifier.

## Provenance

- Book ID: `linux-go-low-level-programming-tsilyurik-ru`
- Source path: `source/book.pdf`
- Source SHA-256: `df8db4893a8ddd656fcaaed7933b1bd639d32bd6cd18547a3b1d103bef7afdd2`
- Chapter title: `Структуры данных, типы и их методы`
- RAG chunk range: `p0216:c01` … `p0222:c01`
- Included chunks: **7**
- PDF page range: **216–222**
- Chapter boundary verified: **yes**
- Boundary evidence:
  - page 216 starts with `Структуры данных, типы и их методы`;
  - page 222 ends the discussion of named return values;
  - page 223 starts `Строки, руны и UNICODE`.

## Main principle

Главный смысл главы — различать:

```text
array value
≠
pointer to array
≠
slice
```

Источник показывает это через observable effects: копирование массива, изменение массива через указатель и изменение элементов backing storage через slice.

## Important observations

- размер массива входит в его тип: `[7]int` и `[8]int` рассматриваются как разные типы;
- array parameter в примере копируется как значение;
- указатель `*arr` позволяет менять исходный массив;
- slice и array не взаимозаменяемы как параметры;
- `len()` позволяет функции узнать длину slice без отдельного size-параметра;
- двумерный slice может иметь строки разной длины;
- функция может возвращать значения разных типов;
- ненужные return values в примере принимаются в `_`;
- именованные результаты позволяют использовать bare `return`.

## Limitations

- Артефакты не исправляют терминологию по внешней спецификации Go.
- Противоречие о «передаче slice по ссылке» зафиксировано отдельно.
- Объяснение через `Stringer` на странице 220 оставлено как source claim.
- Код `garray_c.c` содержит двойное увеличение `i` внутри одной итерации; см. `source-findings.md`.

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
